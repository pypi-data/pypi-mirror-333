from typing import List, Dict, Any, Optional
import os
import anthropic

from .llm_interface import LLMInterface

class AnthropicProvider(LLMInterface):
    """
    Anthropic API-based LLM provider.
    """
    
    def __init__(self, 
                 api_key: Optional[str] = os.environ["ANTHROPIC_API_KEY"], 
                 model: str = "claude-3-7-sonnet-20250219",
                 **kwargs):
        """
        Initialize the Anthropic provider.
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY environment variable)
            model: The model to use (default: claude-3-opus-20240229)
            **kwargs: Additional client initialization parameters
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key must be provided or set as ANTHROPIC_API_KEY environment variable")
        
        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key, **kwargs)
    
    def generate(self, prompt: str, max_tokens: int = 1000, 
                 temperature: float = 0.0, top_p: float = 1.0, 
                 verbose: bool = False, **kwargs) -> str:
        """
        Generate a response from a single prompt using Anthropic API.
        
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
        if verbose:
            print(f"Generating with Anthropic model {self.model}, prompt: {prompt[:50]}...")
        
        # Format the prompt for Anthropic's API
        if not prompt.startswith("<|"):  # Not already in Anthropic format
            system_prompt = kwargs.pop("system_prompt", "You are a helpful assistant.")
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        else:
            # Assume it's already properly formatted for the API
            system_prompt = ""
            messages = [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        
        response = self.client.messages.create(
            model=self.model,
            messages=messages,
            system=system_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            **kwargs
        )
        
        return response.content[0].text
    
    def batch_generate(self, prompts: List[str], max_tokens: int = 1000,
                       temperature: float = 0.0, top_p: float = 1.0,
                       verbose: bool = False, **kwargs) -> List[str]:
        """
        Generate responses from multiple prompts using Anthropic API.
        Note: This makes sequential API calls as Anthropic doesn't support true batching.
        
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
        responses = []
        for i, prompt in enumerate(prompts):
            if verbose:
                print(f"Generating response {i+1}/{len(prompts)}")
            response = self.generate(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                verbose=verbose,
                **kwargs
            )
            responses.append(response)
        
        return responses 