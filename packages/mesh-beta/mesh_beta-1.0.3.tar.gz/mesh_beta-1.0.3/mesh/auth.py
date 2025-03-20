"""
Authentication Module for Mesh SDK

This module handles authentication with the Mesh backend API.
"""

import os
import sys
import time
import json
import logging
import webbrowser
import urllib.parse
import requests
from typing import Dict, Any, Optional, Tuple, List, Union

# Import and re-export token manager functions
from .token_manager import store_token, get_token, is_token_valid, clear_token, load_token

# Import configuration
from .config import (
    get_config, 
    get_auth_config_endpoint, 
    get_auth_url_endpoint, 
    get_token_exchange_endpoint,
    get_token_refresh_endpoint
)

# Configure logging
logger = logging.getLogger("mesh.auth")

# Create a cache for Auth0 configuration
AUTH0_CONFIG_CACHE = {}

def get_auth0_config() -> Dict[str, str]:
    """
    Get Auth0 configuration from the backend.
    
    Returns:
        Dict[str, str]: Auth0 configuration including domain, client_id, and audience
    """
    global AUTH0_CONFIG_CACHE
    
    # Return cached config if available and not empty
    if AUTH0_CONFIG_CACHE and all(AUTH0_CONFIG_CACHE.values()):
        return AUTH0_CONFIG_CACHE
    
    try:
        # Fetch Auth0 configuration from the backend
        response = requests.get(get_auth_config_endpoint())
        response.raise_for_status()
        
        config = response.json()
        if config and "domain" in config and "client_id" in config:
            # Update cache
            AUTH0_CONFIG_CACHE = config
            return config
        else:
            logger.error("Invalid Auth0 configuration received from backend")
            return {}
    except Exception as e:
        logger.error(f"Failed to fetch Auth0 configuration from backend: {str(e)}")
        return {}

def get_auth_url() -> str:
    """
    Get authorization URL from the backend.
    
    Returns:
        str: Authorization URL
    """
    try:
        # Use the backend URL generation endpoint
        auth_url_endpoint = get_auth_url_endpoint()
        
        # Prepare data for URL generation
        url_data = {
            "redirect_uri": f"http://localhost:{get_config('AUTH0_CALLBACK_PORT', '8000')}/callback",
            "scope": "openid profile email offline_access",
            "state": "auth0_" + str(int(time.time()))
        }
        
        # Make request to backend
        response = requests.post(auth_url_endpoint, json=url_data)
        response.raise_for_status()
        
        url_response = response.json()
        if not url_response or "auth_url" not in url_response:
            logger.error("No auth_url in response")
            return ""
        
        return url_response["auth_url"]
    except Exception as e:
        logger.error(f"Error getting auth URL: {str(e)}")
        return ""

def exchange_code_for_token(code: str) -> Dict[str, Any]:
    """
    Exchange authorization code for token using the backend endpoint.

    Args:
        code: Authorization code from Auth0
        
    Returns:
        dict: Token data or empty dict if exchange failed
    """
    try:
        exchange_url = get_token_exchange_endpoint()
        # Use configurable callback URI instead of hardcoded localhost
        callback_uri = get_config("AUTH0_CALLBACK_URI", f"http://localhost:{get_config('AUTH0_CALLBACK_PORT', '8000')}/callback")
        exchange_data = {
            "code": code,
            "redirect_uri": callback_uri
        }
        response = requests.post(exchange_url, json=exchange_data)
        response.raise_for_status()
        token_data = response.json()
        if "expires_in" in token_data and "expires_at" not in token_data:
            token_data["expires_at"] = int(time.time()) + token_data["expires_in"]
        return token_data
    except Exception as e:
        logger.error(f"Error exchanging code for token: {str(e)}")
        return {}

def refresh_auth_token(refresh_token=None):
    """
    Refresh an Auth0 token using the refresh token.
    
    Args:
        refresh_token: Refresh token to use
        
    Returns:
        dict: New token data or None if refresh failed
    """
    # If no refresh token was provided, try to get it from the stored token
    if not refresh_token:
        token_data = get_token()
        if token_data:
            refresh_token = token_data.get("refresh_token")
    
    # If we still don't have a refresh token, we can't refresh
    if not refresh_token:
        logger.warning("No refresh token available")
        return None
    
    # If the refresh token is empty, we can't refresh
    if not refresh_token.strip():
        logger.warning("Refresh token is empty")
        return None
    
    logger.info("Attempting to refresh token")
    
    try:
        # Try to refresh using the backend
        response = requests.post(
            get_token_refresh_endpoint(),
            json={"refresh_token": refresh_token},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            
            # Add expires_at for convenience
            if "expires_in" in token_data:
                token_data["expires_at"] = int(time.time()) + token_data["expires_in"]
            
            # Store the new token
            store_token(token_data)
            
            logger.info("Successfully refreshed token")
            return token_data
        else:
            logger.warning(f"Token refresh failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.warning(f"Token refresh failed: {str(e)}")
        return None
    
    return None

def authenticate(timeout: int = 300) -> Dict[str, Any]:
    """
    Authenticate with the Mesh backend.
    
    This function checks for an existing valid token first, then tries to
    refresh an expired token, and returns None if those fail.
    The actual authentication happens in the MeshClient._authenticate_backend_driven method.
    
    Args:
        timeout: Timeout in seconds for authentication
        
    Returns:
        dict: Token data or None if authentication failed
    """
    # Check if we already have a valid token
    token_data = get_token()
    
    # If token exists but is invalid, try to refresh it first
    if token_data and not is_token_valid(token_data):
        logger.info("Token exists but is invalid or expired, attempting to refresh")
        try:
            # Try refreshing the token
            refreshed_token = refresh_auth_token(refresh_token=token_data.get("refresh_token"))
            
            if refreshed_token and is_token_valid(refreshed_token):
                logger.info("Successfully refreshed token")
                return refreshed_token
            else:
                logger.info("Token refresh failed, will proceed with re-authentication")
        except Exception as e:
            logger.warning(f"Error during token refresh: {str(e)}. Will proceed with re-authentication.")
    elif is_token_valid(token_data):
        logger.info("Using existing valid token")
        return token_data
    
    # Return None to signal that the client should use backend-driven authentication
    return None 

def authenticate():
    """Placeholder authentication function. Use MeshClient._authenticate_backend_driven() instead."""
    raise NotImplementedError("Please use MeshClient._authenticate_backend_driven for authentication.")

def authenticate_device_flow():
    """Placeholder device flow authentication function. Device flow is not implemented in this SDK."""
    raise NotImplementedError("Device flow authentication is not implemented in this SDK.") 