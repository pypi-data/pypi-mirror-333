"""
Mesh API Client SDK

This package provides a simple, powerful interface to the Mesh API.
"""

import os
import sys
import logging
from typing import Dict, Any, Optional, List, Union

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mesh")

# Export client classes for advanced usage
from .client import MeshClient
from .zkp_client import MeshZKPClient
from .auto_refresh_client import AutoRefreshMeshClient

# Export model constants
from .models import OpenAI, Anthropic, Provider, get_best_model, get_fastest_model, get_cheapest_model

# Create a singleton client instance
_client = None

def _get_client() -> MeshClient:
    """Get or create a singleton client instance with automatic authentication
    
    Returns:
        MeshClient: An authenticated client with auto-refresh capabilities
    """
    global _client
    
    # Return existing client if available
    if _client is not None:
        return _client
    
    # Import here to avoid circular imports
    from .token_manager import get_token, is_token_valid
    from .auth import authenticate, authenticate_device_flow
    
    # Check for existing token
    token_data = get_token()
    
    # Authenticate if needed
    if not token_data or not is_token_valid(token_data):
        # Always use device code flow to avoid browser-based auth issues
        logger.info("Authentication required for Mesh SDK")
        # Explicitly use device code flow and don't fall back to browser-based auth
        token_data = authenticate_device_flow()
        
        if not token_data:
            logger.warning("Authentication failed")
            print("\nAuthentication failed. Please run 'mesh-auth' manually to authenticate.")
            print("See the README for configuration instructions.")
            raise RuntimeError("Authentication failed. Please run 'mesh-auth' from the command line.")
        
        logger.info("Authentication successful")
        print("\n✅ Authentication successful! You can now use the Mesh SDK.")
    else:
        logger.info("Using existing valid token")
    
    # Create client with the token
    from .auto_refresh_client import AutoRefreshMeshClient
    _client = AutoRefreshMeshClient()
    _client.token_data = token_data
    
    return _client

# =========================
# Simplified API Functions
# =========================

def chat(message: str, model: Optional[str] = None, provider: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    """Send a chat message to an AI model
    
    Args:
        message: The message to send
        model: The model to use (e.g. "gpt-4", "claude-3-5-sonnet")
        provider: The provider to use (e.g. "openai", "anthropic")
        **kwargs: Additional options for the chat request
        
    Returns:
        dict: The chat response
    """
    client = _get_client()
    return client.chat(message, model=model, provider=provider, **kwargs)

def store_key(key_name: str, key_value: str, user_id: str = None) -> Dict[str, Any]:
    """Store a key in the Mesh API
    
    Args:
        key_name: Name of the key to store
        key_value: Value of the key to store
        user_id: Optional User ID to associate with the key. If not provided, extracted from auth token.
        
    Returns:
        dict: Result of the operation
    """
    client = _get_client()
    return client.store_key(key_name=key_name, key_value=key_value, user_id=user_id)

def get_key(key_name: str, user_id: str = None) -> Optional[str]:
    """Get a key from the Mesh API
    
    Args:
        key_name: Name of the key to retrieve
        user_id: Optional User ID to retrieve key for. If not provided, extracted from auth token.
        
    Returns:
        Optional[str]: The key value if found, or None if not found
    """
    client = _get_client()
    return client.get_key(key_name=key_name, user_id=user_id)

def store_key_zkp(key_name: str, key_value: str, user_id: str = None) -> Dict[str, Any]:
    """Store a key using Zero-Knowledge Proofs
    
    Args:
        key_name: Name of the key to store
        key_value: Value of the key to store
        user_id: Optional User ID to associate with the key. If not provided, extracted from auth token.
        
    Returns:
        dict: Result of the operation
    """
    from .zkp_client import MeshZKPClient
    client = MeshZKPClient()
    
    # Transfer authentication from singleton client
    main_client = _get_client()
    client.auth_token = main_client.auth_token
    
    return client.store_key_zkp(key_name=key_name, key_value=key_value, user_id=user_id)

def verify_key(key_name: str, key_value: str, user_id: str = None) -> bool:
    """Verify a key using Zero-Knowledge Proofs
    
    Args:
        key_name: Name of the key to verify
        key_value: Value of the key to verify
        user_id: Optional User ID to verify key for. If not provided, extracted from auth token.
        
    Returns:
        bool: True if key verified successfully, False otherwise
    """
    from .zkp_client import MeshZKPClient
    client = MeshZKPClient()
    
    # Transfer authentication from singleton client
    main_client = _get_client()
    client.auth_token = main_client.auth_token
    
    result = client.verify_key(key_name=key_name, key_value=key_value, user_id=user_id)
    return result.get("verified", False)

def list_keys(user_id: str = None) -> List[str]:
    """List all keys stored for a user
    
    Args:
        user_id: Optional User ID to list keys for. If not provided, extracted from auth token.
        
    Returns:
        List[str]: A list of key names (without the user_id prefix)
    """
    client = _get_client()
    return client.list_keys(user_id=user_id)

# Export simplified API functions and client classes
__all__ = [
    # Simplified API
    'chat',
    'store_key',
    'get_key',
    'store_key_zkp',
    'verify_key',
    'list_keys',
    
    # Client classes for advanced usage
    'MeshClient',
    'MeshZKPClient',
    'AutoRefreshMeshClient'
] 