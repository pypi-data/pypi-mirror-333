from abc import ABC, abstractmethod
from typing import List, Tuple, Dict, Any, Optional

class LLMInterface(ABC):
    """
    Abstract interface for LLM providers.
    All LLM implementations (MLX, OpenAI, Anthropic) should implement this interface.
    """
    
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = 1000, 
                 temperature: float = 0.0, top_p: float = 1.0, 
                 verbose: bool = False, **kwargs) -> str:
        """
        Generate a response from a single prompt.
        
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
        pass
    
    @abstractmethod
    def batch_generate(self, prompts: List[str], max_tokens: int = 1000,
                       temperature: float = 0.0, top_p: float = 1.0,
                       verbose: bool = False, **kwargs) -> List[str]:
        """
        Generate responses from multiple prompts in parallel.
        
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
        pass
    
    @staticmethod
    def create(provider: str, **kwargs) -> 'LLMInterface':
        """
        Factory method to create an LLM provider instance.
        
        Args:
            provider: The provider name ('mlx', 'openai', 'anthropic')
            **kwargs: Provider-specific initialization parameters
            
        Returns:
            An instance of the requested LLM provider
        """
        if provider.lower() == 'mlx':
            from .mlx_provider import MLXProvider
            return MLXProvider(**kwargs)
        elif provider.lower() == 'openai':
            from .openai_provider import OpenAIProvider
            return OpenAIProvider(**kwargs)
        elif provider.lower() == 'anthropic':
            from .anthropic_provider import AnthropicProvider
            return AnthropicProvider(**kwargs)
        else:
            raise ValueError(f"Unknown LLM provider: {provider}") 