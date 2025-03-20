import mlx.core as mx
import mlx.nn as nn
from mlx_lm import load, generate
from mlx_lm.tokenizer_utils import TokenizerWrapper
from mlx_lm.utils import apply_repetition_penalty
import time
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Union

from .llm_interface import LLMInterface
from .mlx_generation import batch_generate as mlx_batch_generate

class MLXProvider(LLMInterface):
    """
    MLX-based LLM provider for local Llama 3.1 inference.
    """
    
    def __init__(self, model_name: str = "mlx-community/Meta-Llama-3.1-8B-Instruct-8bit", **kwargs):
        """
        Initialize the MLX provider with a specific model.
        
        Args:
            model_name: The name of the MLX model to load
            **kwargs: Additional model loading parameters
        """
        self.model_name = model_name
        self.model, self.tokenizer = load(model_name, **kwargs)
    
    def generate(self, prompt: str, max_tokens: int = 1000, 
                 temperature: float = 0.0, top_p: float = 1.0, 
                 verbose: bool = False, **kwargs) -> str:
        """
        Generate a response from a single prompt using MLX.
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 = deterministic)
            top_p: Nucleus sampling parameter
            verbose: Whether to print debug information
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Generated text response
        """
        return generate(
            self.model, 
            self.tokenizer,
            prompt=prompt,
            max_tokens=max_tokens,
            temp=temperature,
            top_p=top_p,
            verbose=verbose,
            **kwargs
        )
    
    def batch_generate(self, prompts: List[str], max_tokens: int = 1000,
                       temperature: float = 0.0, top_p: float = 1.0,
                       verbose: bool = False, **kwargs) -> List[str]:
        """
        Generate responses from multiple prompts in parallel using MLX.
        
        Args:
            prompts: List of input prompts
            max_tokens: Maximum number of tokens to generate per response
            temperature: Sampling temperature (0.0 = deterministic)
            top_p: Nucleus sampling parameter
            verbose: Whether to print debug information
            **kwargs: Additional provider-specific parameters
            
        Returns:
            List of generated text responses
        """
        return mlx_batch_generate(
            self.model,
            self.tokenizer,
            prompts=prompts,
            max_tokens=max_tokens,
            temp=temperature,
            top_p=top_p,
            verbose=verbose,
            **kwargs
        ) 