from typing import List, Dict, Any, Optional
import os
from openai import OpenAI

from .llm_interface import LLMInterface

class OpenAIProvider(LLMInterface):
    """
    OpenAI API-based LLM provider.
    """
    
    def __init__(self, 
                 api_key: Optional[str] = os.environ["OPENAI_API_KEY"], 
                 model: str = "gpt-4o",
                 **kwargs):
        """
        Initialize the OpenAI provider.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY environment variable)
            model: The model to use (default: gpt-4o)
            **kwargs: Additional client initialization parameters
        """
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided or set as OPENAI_API_KEY environment variable")
        
        self.model = model
        self.client = OpenAI(api_key=self.api_key, **kwargs)
    
    def generate(self, prompt: str, max_tokens: int = 1000, 
                 temperature: float = 0.0, top_p: float = 1.0, 
                 verbose: bool = False, **kwargs) -> str:
        """
        Generate a response from a single prompt using OpenAI API.
        
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
            print(f"Generating with OpenAI model {self.model}, prompt: {prompt[:50]}...")
        
        # Check if the prompt is already in chat format
        if isinstance(prompt, str) and not prompt.startswith("{") and not "<|" in prompt:
            # Convert to chat format
            messages = [{"role": "user", "content": prompt}]
        else:
            # Assume it's already properly formatted for the API
            messages = [{"role": "user", "content": prompt}]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            **kwargs
        )
        
        return response.choices[0].message.content
    
    def batch_generate(self, prompts: List[str], max_tokens: int = 1000,
                       temperature: float = 0.0, top_p: float = 1.0,
                       verbose: bool = False, **kwargs) -> List[str]:
        """
        Generate responses from multiple prompts using OpenAI API.
        Note: This makes sequential API calls as OpenAI doesn't support true batching.
        
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