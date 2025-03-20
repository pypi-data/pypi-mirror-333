"""
Mesh SDK Model Constants

This module provides constants for model names to make it easier to use specific models
without having to remember exact model names.
"""

class OpenAI:
    """OpenAI model constants"""
    
    # GPT-4o models
    GPT4O = "gpt-4o"
    GPT4O_LATEST = "gpt-4o-2024-11-20"
    GPT4O_MINI = "gpt-4o-mini"
    
    # GPT-4.5 models
    GPT45 = "gpt-4.5-preview"
    
    # GPT-4 models
    GPT4 = "gpt-4"
    GPT4_TURBO = "gpt-4-turbo"
    
    # GPT-3.5 models
    GPT3_5 = "gpt-3.5-turbo"
    
    # o1 and o3 models
    O1 = "o1"
    O1_MINI = "o1-mini"
    O3_MINI = "o3-mini"

class Anthropic:
    """Anthropic model constants"""
    
    # Claude 3.7 models
    CLAUDE_3_7_SONNET = "claude-3-7-sonnet-20250219"
    
    # Claude 3.5 models
    CLAUDE_35_SONNET_NEW = "claude-3-5-sonnet-20241022"
    CLAUDE_35_HAIKU = "claude-3-5-haiku-20241022"
    CLAUDE_35_SONNET_OLD = "claude-3-5-sonnet-20240620"
    
    # Claude 3 models
    CLAUDE_3_OPUS = "claude-3-opus-20240229"
    CLAUDE_3_SONNET = "claude-3-sonnet-20240229"
    CLAUDE_3_HAIKU = "claude-3-haiku-20240307"
    
    # Claude 2 models
    CLAUDE_21 = "claude-2.1"
    CLAUDE_20 = "claude-2.0"
    
    # Default Claude model (alias for latest and best model)
    CLAUDE = CLAUDE_3_7_SONNET

class Provider:
    """Provider constants"""
    
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

# Helper functions for common model combinations
def get_best_model(provider: str = None) -> str:
    """Get the best model for a provider
    
    Args:
        provider: The provider name (default: from configuration)
        
    Returns:
        str: The best model for the provider
    """
    from .config import get_default_provider
    
    provider = provider or get_default_provider()
    
    if provider.lower() == Provider.OPENAI:
        return OpenAI.GPT4O
    elif provider.lower() == Provider.ANTHROPIC:
        return Anthropic.CLAUDE_3_7_SONNET
    else:
        return OpenAI.GPT4O  # Default to OpenAI

def get_fastest_model(provider: str = None) -> str:
    """Get the fastest model for a provider
    
    Args:
        provider: The provider name (default: from configuration)
        
    Returns:
        str: The fastest model for the provider
    """
    from .config import get_default_provider
    
    provider = provider or get_default_provider()
    
    if provider.lower() == Provider.OPENAI:
        return OpenAI.GPT4O_MINI
    elif provider.lower() == Provider.ANTHROPIC:
        return Anthropic.CLAUDE_35_HAIKU
    else:
        return OpenAI.GPT4O_MINI  # Default to OpenAI

def get_cheapest_model(provider: str = None) -> str:
    """Get the cheapest model for a provider
    
    Args:
        provider: The provider name (default: from configuration)
        
    Returns:
        str: The cheapest model for the provider
    """
    from .config import get_default_provider
    
    provider = provider or get_default_provider()
    
    if provider.lower() == Provider.OPENAI:
        return OpenAI.GPT35
    elif provider.lower() == Provider.ANTHROPIC:
        return Anthropic.CLAUDE_35_HAIKU
    else:
        return OpenAI.GPT35  # Default to OpenAI 