import mlx.core as mx
import mlx.nn as nn
from mlx_lm import load
from mlx_lm.tokenizer_utils import TokenizerWrapper
from mlx_lm.utils import apply_repetition_penalty
import time
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Union

# mlx batch generation code from MLX Para-LLM (Will Brown)
# https://github.com/willccbb/mlx_parallm/tree/main

class BatchedKVCache:

    def __init__(self, head_dim, n_kv_heads, batch_size=1):
        self.n_kv_heads = n_kv_heads
        self.head_dim = head_dim
        self.batch_size = batch_size
        self.keys = None
        self.values = None
        self.offset = 0
        self.step = 256

    def update_and_fetch(self, keys, values):
        prev = self.offset
        if self.keys is None or (prev + keys.shape[2]) > self.keys.shape[2]:
            n_steps = (self.step + keys.shape[2] - 1) // self.step
            shape = (self.batch_size, self.n_kv_heads, n_steps * self.step, self.head_dim)
            new_k = mx.zeros(shape, keys.dtype)
            new_v = mx.zeros(shape, values.dtype)
            if self.keys is not None:
                if prev % self.step != 0:
                    self.keys = self.keys[..., :prev, :]
                    self.values = self.values[..., :prev, :]
                self.keys = mx.concatenate([self.keys, new_k], axis=2)
                self.values = mx.concatenate([self.values, new_v], axis=2)
            else:
                self.keys, self.values = new_k, new_v

        self.offset += keys.shape[2]
        self.keys[..., prev : self.offset, :] = keys
        self.values[..., prev : self.offset, :] = values
        return self.keys[..., : self.offset, :], self.values[..., : self.offset, :]
    

def top_p_sampling(logits: mx.array, top_p: float, temperature: float, axis: int = -1) -> mx.array:
    """
    Apply top-p (nucleus) sampling to logits.

    Args:
        logits: The logits from the model's output.
        top_p: The cumulative probability threshold for top-p filtering.
        temperature: Temperature parameter for softmax distribution reshaping.
    Returns:
        token selected based on the top-p criterion.
    """
    # Apply temperature and compute softmax
    probs = mx.softmax(logits / temperature, axis=axis)
    
    # Sort probs in descending order
    sorted_indices = mx.argsort(-probs, axis=axis)
    sorted_probs = mx.take_along_axis(probs, sorted_indices, axis=axis)
    
    # Compute cumulative probabilities
    cumulative_probs = mx.cumsum(sorted_probs, axis=axis)
    
    # Create a mask for probs above the threshold
    mask = cumulative_probs <= top_p
    
    # Apply the mask to the sorted probabilities
    masked_probs = sorted_probs * mask
    
    # Normalize the masked probabilities
    normalized_probs = masked_probs / mx.sum(masked_probs, axis=axis, keepdims=True)
    
    # Sample from the normalized probabilities
    sampled_indices = mx.random.categorical(mx.log(normalized_probs), axis=axis)
    
    # Gather the original token indices
    tokens = mx.take_along_axis(sorted_indices, mx.expand_dims(sampled_indices, axis=axis), axis=axis)
    
    return tokens #.squeeze(axis=axis)


def generate_step(
    prompts: mx.array,
    model: nn.Module,
    temp: float = 0.0,
    repetition_penalty: Optional[float] = None,
    repetition_context_size: Optional[int] = 20,
    top_p: float = 1.0,
    logit_bias: Optional[Dict[int, float]] = None,
) -> Generator[Tuple[mx.array, mx.array], None, None]:
    """
    A generator producing token ids based on the given prompt from the model.

    Args:
        prompt (mx.array): The input prompt.
        model (nn.Module): The model to use for generation.
        temp (float): The temperature for sampling, if 0 the argmax is used.
          Default: ``0``.
        repetition_penalty (float, optional): The penalty factor for repeating
          tokens.
        repetition_context_size (int, optional): The number of tokens to
          consider for repetition penalty. Default: ``20``.
        top_p (float, optional): Nulceus sampling, higher means model considers
          more less likely words.

    Yields:
        Generator[Tuple[mx.array, mx.array]]: A generator producing
        one token and probability per call.
    """

    def sample(logits: mx.array) -> Tuple[mx.array, float]:
        if logit_bias:
            indices = mx.array(list(logit_bias.keys()))
            values = mx.array(list(logit_bias.values()))
            logits[:, indices] += values
        softmax_logits = mx.softmax(logits, axis=-1)

        if temp == 0:
            tokens = mx.argmax(logits, axis=-1, keepdims=True)
        else:
            if top_p > 0 and top_p < 1.0:
                tokens = top_p_sampling(logits, top_p, temp)
            else:
                scaled_logits = logits * (1 / temp)
                tokens = mx.random.categorical(logits * (1 / temp), axis=-1)
                if scaled_logits.ndim > 1:
                    tokens = mx.expand_dims(tokens, axis=-1)

        probs = softmax_logits[0, tokens]
        return tokens, probs

    if repetition_penalty:
        raise NotImplementedError("repetition_penalty not supported.")

    if repetition_penalty and (
        repetition_penalty < 0 or not isinstance(repetition_penalty, float)
    ):
        raise ValueError(
            f"repetition_penalty must be a non-negative float, got {repetition_penalty}"
        )

    # (bs, ntoks)
    y = prompts
    kv_heads = (
        [model.n_kv_heads] * len(model.layers)
        if isinstance(model.n_kv_heads, int)
        else model.n_kv_heads
    )

    cache = [BatchedKVCache(model.head_dim, n, y.shape[0]) for n in kv_heads]

    repetition_context = prompts

    if repetition_context_size and repetition_penalty:
        repetition_context = repetition_context[:,-repetition_context_size:]

    def _step(y):
        nonlocal repetition_context
        logits = model(y, cache=cache)
        logits = logits[:, -1, :]

        if repetition_penalty:
            logits = apply_repetition_penalty(
                logits, repetition_context, repetition_penalty
            )
            y, probs = sample(logits)
            repetition_context = mx.concatenate([repetition_context, y])
        else:
            y, probs = sample(logits)

        if repetition_context_size:
            if repetition_context.shape[1] > repetition_context_size:
                repetition_context = repetition_context[:,-repetition_context_size:]
        return y, probs

    y, p = _step(y)
    mx.async_eval(y)
    while True:
        next_y, next_p = _step(y)
        mx.async_eval(next_y)
        mx.eval(y)
        yield y, p
        y, p = next_y, next_p

def batch_generate(
    model,
    tokenizer,
    prompts: List[str],
    max_tokens: int = 100,
    verbose: bool = False,
    format_prompts: bool = True,
    formatter: Optional[Callable] = None,
    **kwargs,
) -> Union[str, Generator[str, None, None]]:
    """
    Generate a complete response from the model.

    Args:
       model (nn.Module): The language model.
       tokenizer (PreTrainedTokenizer): The tokenizer.
       prompt (str): The string prompt.
       max_tokens (int): The maximum number of tokens. Default: ``100``.
       verbose (bool): If ``True``, print tokens and timing information.
           Default: ``False``.
       formatter (Optional[Callable]): A function which takes a token and a
           probability and displays it.
       kwargs: The remaining options get passed to :func:`generate_step`.
          See :func:`generate_step` for more details.
    """
    if not isinstance(tokenizer, TokenizerWrapper):
        tokenizer = TokenizerWrapper(tokenizer)

    if verbose:
        print("=" * 10)
    
    if format_prompts:
        prompts_fm = [[{"role": "user", "content": prompt}] for prompt in prompts]
        prompts_fm = [tokenizer.apply_chat_template(prompt, add_generation_prompt=True, tokenize=False) for prompt in prompts_fm]
    else:
        prompts_fm = prompts

    # left-padding for batched generation
    tokenizer._tokenizer.padding_side = 'left'
    if tokenizer.pad_token is None:
        tokenizer._tokenizer.pad_token = tokenizer.eos_token
        tokenizer._tokenizer.pad_token_id = tokenizer.eos_token_id

    prompts_toks = mx.array(tokenizer._tokenizer(prompts_fm, padding=True)['input_ids'])
    tic = time.perf_counter()

    output_toks = []
    for (tokens, _), n in zip(
        generate_step(prompts_toks, model, **kwargs),
        range(max_tokens),
    ): 
        if n == 0:
            prompt_time = time.perf_counter() - tic
            tic = time.perf_counter()
        output_toks.append(tokens)
    output_toks = mx.concatenate(output_toks, axis=1)

    responses = [response.split(tokenizer.eos_token)[0].split(tokenizer.pad_token)[0] for response in tokenizer.batch_decode(output_toks.tolist())]
    if verbose:
        gen_time = time.perf_counter() - tic
        prompt_tps = prompts_toks.size / prompt_time
        gen_tps = output_toks.size / gen_time
        print(f"Prompt: {prompt_tps:.3f} tokens-per-sec")
        print(f"Generation: {gen_tps:.3f} tokens-per-sec")
        for prompt, response in zip(prompts, responses):
            print("=" * 10)
            print("Prompt:", prompt)
            print(response)
            
    return responses