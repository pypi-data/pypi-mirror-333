"""
Mesh API Client

This module provides a comprehensive client for interacting with the Mesh API,
including key management, Zero-Knowledge Proofs, chat completions, and usage tracking.

The client is designed to handle both the current API structure and legacy endpoints
for backward compatibility:

- Current API Endpoints: Primarily under `/api/v1/` 
  - `/api/v1/chat/completions` - Primary chat endpoint
  - `/api/v1/completions` - Text completions endpoint
  - `/api/v1/storeKeyZKP` - Store key with ZKP
  - `/api/v1/getCommitment` - Get key commitment
  - `/api/v1/getChallenge` - Get a challenge for verification
  - `/api/v1/verifyProof` - Verify a proof

- Legacy Endpoints: Under `/v1/mesh/` 
  - `/v1/mesh/chat` - Legacy chat endpoint
  - `/v1/mesh/complete` - Legacy completions endpoint
  - `/v1/mesh/storeKey` - Legacy key storage (non-ZKP)
  - `/v1/mesh/getKey` - Legacy key retrieval (non-ZKP)

The client uses a fallback strategy for chat endpoints, trying them in order
until a successful response is received. This ensures compatibility with
different server configurations.

Authentication is handled automatically, with support for:
1. Direct token authentication (providing auth_token)
2. Browser-based Auth0 authentication
3. Token persistence between sessions

Key Features:
- ZKP-based key management
- Legacy key storage and retrieval
- Chat completions with multiple AI providers (OpenAI, Anthropic)
- Extended thinking support for Claude 3.7 models
- Robust error handling and logging
- Token validation and refreshing
"""

import json
import os
import time
import hashlib
import logging
import requests
from typing import Dict, Any, Optional, List, Set, Union

# Import configuration
from .config import (
    get_config, is_debug_enabled, get_default_model, get_default_provider,
    is_thinking_enabled, get_default_thinking_budget, get_default_thinking_max_tokens,
    get_default_model_with_override, get_all_config
)

# Import and re-export token manager functions
from .token_manager import store_token, get_token, is_token_valid
from .auth import refresh_auth_token

# Set up logging
logger = logging.getLogger("mesh_client")
logger.setLevel(logging.WARNING)  # Change from INFO to WARNING to reduce verbosity
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Disable logging from the requests library
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Default configuration
DEFAULT_CONFIG = {
    "normalize_response": True,
    "original_response": False,  # For backward compatibility
    "return_content_only": True,  # New default behavior to return just the content string
    "debug": False  # Add debug flag to control logging
}

# Default models for providers
DEFAULT_MODELS = {
    "openai": "gpt-4o",  # Updated default to GPT-4o
    "anthropic": "claude-3-opus-20240229"
}

# Model aliases for easier reference
MODEL_ALIASES = {
    # OpenAI aliases
    "gpt4": "gpt-4",
    "gpt4o": "gpt-4o",
    "gpt4.5": "gpt-4.5-preview",
    "gpt45": "gpt-4.5-preview",
    "gpt3": "gpt-3.5-turbo",
    "gpt35": "gpt-3.5-turbo",
    "gpt3.5": "gpt-3.5-turbo",
    "gpt4omni": "gpt-4o",
    
    # Claude 3.7 aliases
    "claude": "claude-3-7-sonnet-20250219",  # Default to latest Claude
    "claude37": "claude-3-7-sonnet-20250219",
    "claude37sonnet": "claude-3-7-sonnet-20250219",
    "claude37s": "claude-3-7-sonnet-20250219",
    "claude3.7": "claude-3-7-sonnet-20250219",
    "claude-37": "claude-3-7-sonnet-20250219",
    "claude-3-7": "claude-3-7-sonnet-20250219",
    "claude-3.7": "claude-3-7-sonnet-20250219",
    "claude-3.7-sonnet": "claude-3-7-sonnet-20250219",
    
    # Claude 3.5 aliases
    "claude35": "claude-3-5-sonnet-20241022",
    "claude35sonnet": "claude-3-5-sonnet-20241022",
    "claude35s": "claude-3-5-sonnet-20241022",
    "claude3.5": "claude-3-5-sonnet-20241022",
    "claude-35": "claude-3-5-sonnet-20241022",
    "claude-3-5": "claude-3-5-sonnet-20241022",
    "claude-3.5": "claude-3-5-sonnet-20241022",
    "claude-3.5-sonnet": "claude-3-5-sonnet-20241022",
    "claude3.5": "claude-3-5-sonnet-20241022",
    "claude-3.5-s": "claude-3-5-sonnet-20241022",
    "claude3.5s": "claude-3-5-sonnet-20241022",
    "claude3.5-sonnet": "claude-3-5-sonnet-20241022",
    "claude-3.5-sonnet-latest": "claude-3-5-sonnet-20241022",
    "claude-3.5-latest": "claude-3-5-sonnet-20241022",
    
    # Claude 3.5 Haiku aliases
    "claude35haiku": "claude-3-5-haiku-20241022",
    "claude35h": "claude-3-5-haiku-20241022",
    "claude3.5haiku": "claude-3-5-haiku-20241022",
    "claude-35-haiku": "claude-3-5-haiku-20241022",
    "claude-3-5-h": "claude-3-5-haiku-20241022",
    
    # Claude 3 Opus aliases
    "claude3opus": "claude-3-opus-20240229",
    "claudeopus": "claude-3-opus-20240229",
    "claude-3-opus": "claude-3-opus-20240229",
    "claude-opus": "claude-3-opus-20240229",
    
    # Claude 3 Sonnet aliases
    "claude3sonnet": "claude-3-sonnet-20240229",
    "claude3s": "claude-3-sonnet-20240229",
    "claude-3-sonnet": "claude-3-sonnet-20240229",
    "claude-3-s": "claude-3-sonnet-20240229",
    "claude-3.0": "claude-3-sonnet-20240229",
    "claude-sonnet": "claude-3-sonnet-20240229",
    
    # Claude 3 Haiku aliases
    "claude3haiku": "claude-3-haiku-20240307",
    "claude3h": "claude-3-haiku-20240307",
    "claude-3-haiku": "claude-3-haiku-20240307",
    "claude-3-h": "claude-3-haiku-20240307",
    "claude-3.0-haiku": "claude-3-haiku-20240307",
    "claude-haiku": "claude-3-haiku-20240307"
}

# Provider-specific model mappings
PROVIDER_MODELS = {
    "openai": {
        # GPT-4.5 models
        "gpt-4.5-preview": "gpt-4.5-preview",
        "gpt-4.5-preview-2025-02-27": "gpt-4.5-preview-2025-02-27",
        
        # GPT-4o models
        "gpt-4o": "gpt-4o",
        "gpt-4o-2024-08-06": "gpt-4o-2024-08-06",
        "gpt-4o-2024-11-20": "gpt-4o-2024-11-20",
        "gpt-4o-2024-05-13": "gpt-4o-2024-05-13",
        "chatgpt-4o-latest": "chatgpt-4o-latest",
        
        # GPT-4o mini models
        "gpt-4o-mini": "gpt-4o-mini",
        "gpt-4o-mini-2024-07-18": "gpt-4o-mini-2024-07-18",
        
        # o1 and o1-mini models
        "o1": "o1",
        "o1-2024-12-17": "o1-2024-12-17",
        "o1-mini": "o1-mini",
        "o1-mini-2024-09-12": "o1-mini-2024-09-12",
        "o1-preview": "o1-preview",
        "o1-preview-2024-09-12": "o1-preview-2024-09-12",
        
        # o3-mini models
        "o3-mini": "o3-mini",
        "o3-mini-2025-01-31": "o3-mini-2025-01-31",
        
        # Realtime models
        "gpt-4o-realtime-preview": "gpt-4o-realtime-preview",
        "gpt-4o-realtime-preview-2024-12-17": "gpt-4o-realtime-preview-2024-12-17",
        "gpt-4o-realtime-preview-2024-10-01": "gpt-4o-realtime-preview-2024-10-01",
        "gpt-4o-mini-realtime-preview": "gpt-4o-mini-realtime-preview",
        "gpt-4o-mini-realtime-preview-2024-12-17": "gpt-4o-mini-realtime-preview-2024-12-17",
        
        # Audio models
        "gpt-4o-audio-preview": "gpt-4o-audio-preview",
        "gpt-4o-audio-preview-2024-12-17": "gpt-4o-audio-preview-2024-12-17",
        "gpt-4o-audio-preview-2024-10-01": "gpt-4o-audio-preview-2024-10-01",
        "gpt-4o-mini-audio-preview": "gpt-4o-mini-audio-preview",
        "gpt-4o-mini-audio-preview-2024-12-17": "gpt-4o-mini-audio-preview-2024-12-17",
        
        # GPT-4 Turbo and GPT-4
        "gpt-4-turbo": "gpt-4-turbo",
        "gpt-4-turbo-2024-04-09": "gpt-4-turbo-2024-04-09",
        "gpt-4-turbo-preview": "gpt-4-turbo-preview",
        "gpt-4-0125-preview": "gpt-4-0125-preview",
        "gpt-4-1106-preview": "gpt-4-1106-preview",
        "gpt-4": "gpt-4",
        "gpt-4-0613": "gpt-4-0613",
        "gpt-4-0314": "gpt-4-0314",
        
        # GPT-3.5 Turbo
        "gpt-3.5-turbo": "gpt-3.5-turbo",
        "gpt-3.5-turbo-0125": "gpt-3.5-turbo-0125",
        "gpt-3.5-turbo-1106": "gpt-3.5-turbo-1106",
        "gpt-3.5-turbo-instruct": "gpt-3.5-turbo-instruct",
        
        # Base models
        "babbage-002": "babbage-002",
        "davinci-002": "davinci-002"
    },
    "anthropic": {
        # Claude 3.7 models
        "claude-3-7-sonnet-20250219": "claude-3-7-sonnet-20250219",
        
        # Claude 3.5 models
        "claude-3-5-sonnet-20241022": "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022": "claude-3-5-haiku-20241022",
        "claude-3-5-sonnet-20240620": "claude-3-5-sonnet-20240620",
        
        # Claude 3 models
        "claude-3-opus-20240229": "claude-3-opus-20240229",
        "claude-3-sonnet-20240229": "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307": "claude-3-haiku-20240307",
        
        # Claude 2 models
        "claude-2.1": "claude-2.1",
        "claude-2.0": "claude-2.0"
    }
}

class MeshClient:
    """
    Unified client for the Mesh API with key management, ZKP, and chat capabilities
    
    This client provides a unified interface to interact with both the main API server
    and the ZKP microservice. It handles:
    
    1. Basic key management (store/retrieve keys)
    2. Chat functionality with OpenAI and Anthropic models (if available)
    3. Usage tracking and billing
    
    Authentication is handled automatically with support for Auth0 or custom tokens.
    """
    
    def __init__(
        self,
        zkp_server_url=None,
        chat_server_url=None,
        auth_token=None,
        response_format=None,
        auto_refresh=True,
        health_monitor=True
    ):
        """
        Initialize the Mesh client with optional parameters.
        
        Args:
            zkp_server_url: URL of the ZKP microservice (defaults to configured value)
            chat_server_url: URL of the main API server (defaults to configured value)
            auth_token: Auth token for API access (optional, will attempt to get from storage)
            response_format: Default response format for chat (dict or string)
            auto_refresh: Whether to automatically refresh tokens
            health_monitor: Whether to monitor token health
        """
        # Configure logging
        self.logger = logging.getLogger("MeshClient")
        self.logger.setLevel(logging.WARNING)  # Default to WARNING
        
        # Set debug mode if enabled
        if is_debug_enabled():
            self.logger.setLevel(logging.DEBUG)
            self.logger.debug("Debug mode enabled")
            logging.getLogger("mesh_client").setLevel(logging.DEBUG)
        
        # Set up token management
        self._auth_token = None
        self._token_data = None
        self.auto_refresh = auto_refresh
        
        # Set server URLs, using config values as defaults
        self.mesh_api_url = chat_server_url or get_config("MESH_API_URL")
        # Use the provided ZKP server URL or default to the same as the API URL
        self.zkp_server_url = zkp_server_url or self.mesh_api_url
        
        # Use provided auth token or try to load from storage
        if auth_token:
            self.auth_token = auth_token
        else:
            self._load_token()
        
        # Configure response format
        self.config = DEFAULT_CONFIG.copy()
        if response_format:
            if isinstance(response_format, dict):
                self.config.update(response_format)
            elif response_format.lower() == "string":
                self.config["return_content_only"] = True
            elif response_format.lower() == "dict":
                self.config["return_content_only"] = False
        
        # Initialize user profile attributes
        self._profile_checked = False
        self._user_profile = None
        
        # Start token health monitor if enabled
        if health_monitor:
            self._start_token_health_monitor()
    
    def _load_token(self) -> None:
        """Load authentication token from secure storage"""
        from .token_manager import get_token
        
        token_data = get_token()
        if token_data and isinstance(token_data, dict):
            self._token_data = token_data
            self._auth_token = token_data.get("access_token")
            self.logger.debug("Loaded auth token from storage")
    
    def _validate_token(self) -> bool:
        """
        Validate the current authentication token.
        
        Returns:
            bool: True if the token is valid, False otherwise
        """
        from .token_manager import is_token_valid
        
        # No token data or token, not valid
        if not self._token_data or not self._auth_token:
            self.logger.debug("No token data available to validate")
            return False
        
        # Validate the token data
        if is_token_valid(self._token_data):
            return True
        
        # Token is invalid but we have refresh capability
        if self.auto_refresh and "refresh_token" in self._token_data:
            self.logger.debug("Token invalid but refresh capability available")
            return self._refresh_token_with_retry()
        
        # Token is invalid and no refresh capability
        self.logger.debug("Token invalid and no refresh capability")
        return False
    
    def _refresh_token_with_retry(self, max_attempts=3, initial_backoff=1.0):
        """
        Attempt to refresh the authentication token with retries.
        
        Args:
            max_attempts: Maximum number of refresh attempts
            initial_backoff: Initial backoff time in seconds (doubles with each retry)
            
        Returns:
            bool: True if refresh succeeded, False otherwise
        """
        from .auth import refresh_auth_token
        from .token_manager import is_token_valid, store_token
        
        if not self._token_data or "refresh_token" not in self._token_data:
            self.logger.debug("No refresh token available")
            return False
        
        refresh_token = self._token_data.get("refresh_token")
        if not refresh_token:
            self.logger.debug("Refresh token is empty")
            return False
        
        self.logger.debug("Attempting to refresh token")
        
        # Try to refresh the token with retries
        backoff = initial_backoff
        for attempt in range(1, max_attempts + 1):
            try:
                # Use the updated refresh_auth_token function that now uses the backend
                new_token_data = refresh_auth_token(refresh_token=refresh_token)
                
                if new_token_data and "access_token" in new_token_data:
                    # Update the token data and auth token
                    self._token_data = new_token_data
                    self._auth_token = new_token_data.get("access_token")
                    
                    # Store the new token
                    store_token(new_token_data)
                    
                    self.logger.debug("Successfully refreshed token")
                    return True
                else:
                    self.logger.warning(f"Token refresh failed on attempt {attempt}/{max_attempts}")
            except Exception as e:
                self.logger.warning(f"Error during token refresh (attempt {attempt}/{max_attempts}): {str(e)}")
            
            # Don't sleep after the last attempt
            if attempt < max_attempts:
                time.sleep(backoff)
                backoff *= 2  # Exponential backoff
        
        self.logger.error(f"Token refresh failed after {max_attempts} attempts")
        return False

    @property
    def auth_token(self) -> str:
        """Get the direct authentication token"""
        return self._auth_token
    
    @auth_token.setter
    def auth_token(self, value: str):
        """Set the direct authentication token and persist it to disk"""
        self._auth_token = value
        
        # Store the token in the token manager
        if value:
            # Create minimal token data if we only have the token string
            expires_at = time.time() + 3600  # Default expiry of 1 hour
            token_data = {
                "access_token": value,
                "expires_at": expires_at
            }
            
            # Preserve refresh token if we have it
            if self._token_data and "refresh_token" in self._token_data:
                token_data["refresh_token"] = self._token_data["refresh_token"]
                
            # Store in token manager
            store_token(token_data)
            self._token_data = token_data
            
            logger.debug("Stored token in token manager")

    def _get_chat_url(self, endpoint: str) -> str:
        """Get the full URL for a chat endpoint
        
        Args:
            endpoint: The endpoint path (e.g., '/v1/complete')
            
        Returns:
            str: The full URL
        """
        # Ensure endpoint starts with a slash
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
            
        # Handle endpoint normalization
        if endpoint.startswith('/v1/mesh/'):
            # Keep legacy endpoint as-is
            pass
        elif endpoint == '/v1/chat' or endpoint == '/chat':
            # Map to new API path
            endpoint = '/api/v1/chat/completions'
        elif endpoint == '/v1/complete' or endpoint == '/complete':
            # Map to new API path
            endpoint = '/api/v1/completions'
        
        return f"{self.mesh_api_url}{endpoint}"
    
    def _get_zkp_url(self, endpoint: str) -> str:
        """Get the full URL for a ZKP endpoint
        
        Args:
            endpoint: The endpoint path (e.g., '/v1/mesh/storeKeyZKP')
            
        Returns:
            str: The full URL
        """
        # Map old /v1/mesh paths to new /api/v1 paths
        if endpoint.startswith('/v1/mesh/'):
            # Replace '/v1/mesh/' with '/api/v1/'
            normalized_endpoint = endpoint.replace('/v1/mesh/', '/api/v1/')
            logger.debug(f"Mapped {endpoint} to {normalized_endpoint}")
            endpoint = normalized_endpoint
        elif endpoint.startswith('/v1/mesh'):
            # Replace '/v1/mesh' with '/api/v1'
            normalized_endpoint = endpoint.replace('/v1/mesh', '/api/v1')
            logger.debug(f"Mapped {endpoint} to {normalized_endpoint}")
            endpoint = normalized_endpoint
        elif not endpoint.startswith('/api/v1'):
            # If it doesn't already have the /api/v1 prefix and doesn't start with a slash
            if not endpoint.startswith('/'):
                endpoint = '/' + endpoint
            
            # Add the prefix if not already present
            if not endpoint.startswith('/api/v1'):
                normalized_endpoint = '/api/v1' + endpoint
                logger.debug(f"Mapped {endpoint} to {normalized_endpoint}")
                endpoint = normalized_endpoint
        
        return f"{self.zkp_server_url}{endpoint}"

    # =========================
    # Authentication Methods
    # =========================
    
    def _authenticate_with_device_code(self) -> bool:
        """Authenticate using OAuth 2.0 device authorization grant
        
        This doesn't require a browser and works well in headless environments.
        
        Returns:
            bool: True if authentication succeeded
        """
        try:
            # Import here to avoid circular imports
            from .auth import authenticate
            
            logger.info("Attempting device code authentication flow")
            token_data = authenticate(device_flow=True, headless=True)
            
            if token_data and "access_token" in token_data:
                self._token_data = token_data
                self._auth_token = token_data.get("access_token")
                self._store_token_securely(token_data)
                logger.info("Device code authentication successful")
                return True
            else:
                logger.error("Device code authentication failed")
                return False
        except Exception as e:
            logger.error(f"Device code authentication error: {str(e)}")
            return False
    
    def _store_token_securely(self, token_data):
        """Store token with integrity checks
        
        Args:
            token_data (dict): Token data to store
            
        Returns:
            bool: True if token was stored successfully
        """
        if not token_data:
            return False
        
        # Add integrity check hash
        token_with_integrity = token_data.copy()
        token_json = json.dumps(token_data, sort_keys=True)
        import hashlib
        integrity_hash = hashlib.sha256(token_json.encode()).hexdigest()
        token_with_integrity["_integrity_hash"] = integrity_hash
        
        # Add timestamp for versioning
        token_with_integrity["_stored_at"] = time.time()
        
        # Store token using the standard function
        store_token(token_with_integrity)
        
        return True
    
    def _ensure_authenticated(self) -> bool:
        """Comprehensive multi-layered authentication ensuring method
        
        This implements the full multi-layered authentication approach:
        1. Use existing token if valid
        2. Try refresh with retry and multiple endpoints
        3. Try device code auth for headless environments
        4. Fall back to browser auth as last resort
        
        Returns:
            bool: True if authenticated successfully
        """
        # Step 1: Check if we already have a valid token
        if self._auth_token and self._validate_token():
            logger.info("Using existing valid token")
            return True
        
        # Step 2: Try token refresh with retries and alternate endpoints
        if self._token_data and "refresh_token" in self._token_data:
            logger.info("Attempting token refresh with retry")
            if self._refresh_token_with_retry():
                return True
        
        # Step 3: Try device code authentication (headless friendly)
        logger.info("Refresh failed, attempting device code authentication")
        if self._authenticate_with_device_code():
            return True
        
        # Step 4: Last resort - browser-based authentication
        logger.info("Device code failed, falling back to browser authentication")
        try:
            from .auth import authenticate
            token_data = authenticate(headless=False)
            
            if token_data and "access_token" in token_data:
                self._token_data = token_data
                self._auth_token = token_data.get("access_token")
                
                # Store securely with integrity checks
                self._store_token_securely(token_data)
                
                logger.info("Browser authentication successful")
                return True
            else:
                logger.error("Browser authentication failed")
                return False
        except Exception as e:
            logger.error(f"Browser authentication error: {str(e)}")
            return False
    
    def _get_headers(self, additional_headers=None) -> Dict[str, str]:
        """Get headers with authentication if available
        
        Args:
            additional_headers: Additional headers to include
            
        Returns:
            dict: Headers with authentication if available
        """
        headers = {
            "Content-Type": "application/json"
        }
        
        # Add auth token if available
        if self._auth_token:
            # Make sure token doesn't have any accidental whitespace
            token = self._auth_token.strip()
            headers["Authorization"] = f"Bearer {token}"
            # Add debug log of header format
            logger.debug(f"Using Authorization header: Bearer {token[:10]}...")
            
            # Add additional debug info for troubleshooting
            if token.count('.') == 2:
                logger.debug("Token has valid JWT format (3 parts)")
            else:
                logger.warning(f"Token does NOT have valid JWT format (has {token.count('.')+1} parts)")
        else:
            logger.warning("No authentication token available for request")
        
        # Add additional headers
        if additional_headers:
            headers.update(additional_headers)
            
        return headers

    # =========================
    # Basic Key Management
    # =========================
    
    def store_key(self, key_name: str = None, key_value: str = None, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Store a key in the Mesh API
        
        Args:
            key_name: Name of the key (will be stored as {userId}_{key_name})
            key_value: Value of the key to store
            user_id: Optional User ID to associate with the key. If not provided, extracted from auth token.
            
        Returns:
            dict: Result of the operation
        """
        # Validate required parameters
        if not key_name or not key_value:
            return {
                "success": False,
                "error": "Missing required parameters: key_name and key_value must be provided"
            }
            
        # Ensure we're authenticated
        if not self._ensure_authenticated():
            return {
                "success": False,
                "error": "Authentication failed",
                "details": "Could not authenticate with Auth0"
            }
        
        # Get user profile to extract user ID if not provided
        if not user_id:
            if not self._user_profile:
                self._ensure_user_registered()
            
            if self._user_profile and 'id' in self._user_profile:
                user_id = self._user_profile.get('id')
                logger.info(f"Using user ID from profile: {user_id}")
            else:
                return {
                    "success": False,
                    "error": "User ID not provided and could not be extracted from authentication token",
                    "troubleshooting": [
                        "Provide a user_id parameter",
                        "Ensure you are properly authenticated",
                        "Check that the server URL is correct"
                    ]
                }
        
        # Create the storage path: {userId}_{key_name}
        storage_path = f"{user_id}_{key_name}"
        logger.info(f"Storing key with path: {storage_path}")
        
        url = self._get_zkp_url("/api/v1/storeKey")
        
        # Make the request
        headers = self._get_headers()
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json={
                    "userId": user_id,
                    "keyName": storage_path,  # Use the combined path as key name
                    "keyValue": key_value
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                # Add our parameters to the response for verification
                result.update({
                    "storagePath": storage_path,
                    "originalKeyName": key_name
                })
                return result
            else:
                error_data = response.json() if response.content else {}
                return {
                    "success": False,
                    "error": f"Failed to store key: {response.status_code}",
                    "details": error_data
                }
                
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
    
    def get_key(self, key_name: str = None, user_id: Optional[str] = None) -> Optional[str]:
        """Get a key from the Mesh API
        
        Args:
            key_name: Name of the key (will be retrieved using {userId}_{key_name})
            user_id: Optional User ID to retrieve key for. If not provided, extracted from auth token.
            
        Returns:
            str: The key value if found, None if not found or error occurs
        """
        # Validate required parameters
        if not key_name:
            logger.error("Missing required parameter: key_name")
            return None
                
        # Ensure we're authenticated
        if not self._ensure_authenticated():
            logger.error("Authentication failed")
            return None
        
        # Get user profile to extract user ID if not provided
        if not user_id:
            if not self._user_profile:
                self._ensure_user_registered()
            
            if self._user_profile and 'id' in self._user_profile:
                user_id = self._user_profile.get('id')
                logger.info(f"Using user ID from profile: {user_id}")
            else:
                logger.error("Could not determine user ID")
                return None
        
        # Create the storage path: {userId}_{key_name}
        storage_path = f"{user_id}_{key_name}"
        logger.info(f"Retrieving key with path: {storage_path}")
        
        # Make the request
        url = self._get_zkp_url("/api/v1/getKey")
        headers = self._get_headers()
        
        try:
            response = requests.get(
                url,
                headers=headers,
                params={
                    "userId": user_id,
                    "keyName": storage_path  # Use the combined path as key name
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Return None if request failed
                if not result.get("success"):
                    logger.warning(f"Key retrieval failed: {result.get('error', 'Unknown error')}")
                    return None
                    
                # Return the key value - handle both response formats
                key_value = result.get("keyValue") or result.get("key")
                if key_value:
                    logger.info(f"Successfully retrieved key for path: {storage_path}")
                    return key_value
                else:
                    logger.warning(f"No key value found in response for path: {storage_path}")
                    return None
            else:
                logger.error(f"Failed to retrieve key: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            return None
    
    # =========================
    # ZKP Methods
    # =========================
    
    def _generate_nullifier(self, key_name: str, key_value: str) -> str:
        """Generate a nullifier based on the key name and value
        
        Args:
            key_name: Key name
            key_value: Key value
            
        Returns:
            str: Nullifier hash
        """
        # Combine key name and value to create nullifier
        combined = f"{key_name}:{key_value}"
        nullifier = hashlib.sha256(combined.encode()).hexdigest()
        self.last_nullifier = nullifier  # Store for testing
        return nullifier
    
    def _generate_commitment(self, key_value: str, nullifier: str) -> str:
        """Generate a commitment for a key value
        
        Args:
            key_value: The secret key value
            nullifier: A nullifier to prevent replay attacks
            
        Returns:
            A commitment hash
        """
        # Combine the key and nullifier to create a commitment
        combined = f"{key_value}:{nullifier}"
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def _generate_proof(self, nullifier: str, challenge: str, commitment: str) -> str:
        """
        Generate a proof from nullifier, challenge, and commitment
        
        This MUST match the server's proof generation algorithm.
        The server's calculateProof function concatenates the strings and hashes them using SHA-256.
        In Node.js, strings are automatically converted to UTF-8 when hashing.
        
        Args:
            nullifier: The nullifier value
            challenge: The challenge from the server
            commitment: The commitment value
            
        Returns:
            The generated proof as a hex string
        """
        # Debug output
        logger.debug("Client-side proof calculation:")
        logger.debug(f"Nullifier: {nullifier}")
        logger.debug(f"Challenge: {challenge}")
        logger.debug(f"Commitment: {commitment}")
        
        # Concatenate data and generate proof
        # IMPORTANT: This must match the server's algorithm exactly
        # Server does: nullifier + challenge + commitment (direct string concatenation)
        data = nullifier + challenge + commitment
        logger.debug(f"Concatenated data: {data}")
        
        # Create SHA-256 hash
        # In Node.js, crypto.createHash('sha256').update(data) automatically converts strings to UTF-8
        # We'll do the same with encode() in Python
        proof = hashlib.sha256(data.encode('utf-8')).hexdigest()
        
        return proof
    
    def get_challenge(self, user_id: str, key_name: str) -> Dict[str, Any]:
        """Get a challenge from the server for key verification
        
        Args:
            user_id: User ID
            key_name: Key name
            
        Returns:
            Dict containing the challenge response
        """
        # Get a challenge from the server
        url = self._get_zkp_url("/v1/mesh/getChallenge")
        params = {
            "userId": user_id,
            "keyName": key_name
        }
        
        try:
            # Ensure we're authenticated
            self._ensure_authenticated()
            
            # Get headers with authentication
            headers = self._get_headers()
            
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "success": False,
                    "error": f"Failed to get challenge: {response.status_code}",
                    "details": response.json() if response.content else None
                }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
    
    def store_key_zkp(self, user_id: str, key_name: str, key_value: str) -> Dict[str, Any]:
        """Store a key with ZKP commitment
        
        Args:
            user_id: User ID to associate with the key
            key_name: Key name
            key_value: Key value to store
            
        Returns:
            Dict containing the result of the operation
        """
        # Use passed user_id or fall back to instance user_id
        user_id_to_use = user_id or self.user_id
        if not user_id_to_use:
            return {"status": "error", "success": False, "error": "No user ID provided"}
        
        # Ensure user exists
        self.ensure_user_exists(user_id_to_use)
        
        # Generate a nullifier and commitment
        nullifier = self._generate_nullifier(key_name, key_value)
        commitment = self._generate_commitment(key_value, nullifier)
        
        # Store the key with its commitment
        url = self._get_zkp_url("/api/v1/storeKeyZKP")
        logger.debug(f"Using URL for store key ZKP: {url}")
        
        data = {
            "userId": user_id_to_use,
            "keyName": key_name,
            "commitment": commitment
        }
        
        try:
            # Ensure we're authenticated
            self._ensure_authenticated()
            
            # Get headers with authentication
            headers = self._get_headers()
            
            response = requests.post(
                url,
                data=json.dumps(data),
                headers=headers
            )
            
            # Handle different response status codes
            if response.status_code == 200:
                result = response.json()
                # Store the actual parameters used for later verification, 
                # since the server response has them swapped
                result["actualUserId"] = user_id_to_use
                result["actualKeyName"] = key_name
                return {
                    "success": True,
                    "userId": user_id_to_use,
                    "keyName": key_name,
                    "commitment": commitment
                }
            elif response.status_code == 402:
                # Payment required - insufficient credits
                return {
                    "success": False,
                    "error": "Insufficient credits",
                    "details": response.json() if response.content else None
                }
            elif response.status_code == 401 or response.status_code == 403:
                # Authentication error
                return {
                    "success": False,
                    "error": "Authentication failed",
                    "details": response.json() if response.content else "Authentication required"
                }
            else:
                error_data = response.json() if response.content and response.headers.get('content-type', '').startswith('application/json') else {"raw": response.text[:200] if response.text else None}
                return {
                    "success": False,
                    "error": f"Failed to store key: {response.status_code}",
                    "details": error_data
                }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}",
                "type": type(e).__name__
            }
    
    def verify_key(self, user_id: str, key_name: str, key_value: str) -> Dict[str, Any]:
        """
        Verifies a key using Zero-Knowledge Proof (ZKP).

        Args:
            user_id (str): The user ID associated with the key.
            key_name (str): The name of the key to verify.
            key_value (str): The value of the key to verify.

        Returns:
            dict: A dictionary with the verification status and any error information.
        """
        
        # Use passed user_id or fall back to instance user_id
        user_id_to_use = user_id or self.user_id
        if not user_id_to_use:
            return {"status": "error", "success": False, "error": "No user ID provided"}
        
        # Get challenge from server
        challenge_url = self._get_zkp_url("/api/v1/getChallenge")
        logger.debug(f"Using URL for get challenge: {challenge_url}")
        
        try:
            # Ensure we're authenticated
            self._ensure_authenticated()
            
            # Get headers with authentication
            headers = self._get_headers()
            
            response = requests.get(
                challenge_url, 
                params={"userId": user_id_to_use, "keyName": key_name},
                headers=headers
            )
            
            if response.status_code != 200:
                return {"status": "error", "success": False, "error": f"Error getting challenge: {response.status_code} {response.text}"}
            
            challenge = response.json().get("challenge")
        except Exception as e:
            return {"status": "error", "success": False, "error": f"Error getting challenge: {str(e)}"}

        # Generate the nullifier
        nullifier = self._generate_nullifier(key_name, key_value)
        
        # Try to get the stored commitment from the server
        stored_commitment_url = self._get_zkp_url("/api/v1/getCommitment")
        logger.debug(f"Using URL for get commitment: {stored_commitment_url}")
        
        stored_commitment = None
        
        try:
            logger.debug(f"Attempting to fetch commitment from: {stored_commitment_url}")
            response = requests.get(
                stored_commitment_url,
                params={"userId": user_id_to_use, "keyName": key_name},
                headers=headers
            )
            if response.status_code == 200:
                stored_commitment = response.json().get("commitment")
                logger.debug(f"Successfully retrieved stored commitment: {stored_commitment}")
            else:
                logger.debug(f"Unable to get stored commitment (status: {response.status_code}), using local calculation")
                logger.debug(f"Response: {response.text}")
        except Exception as e:
            logger.debug(f"Error getting stored commitment: {str(e)}, using local calculation")
        
        # If we couldn't get the stored commitment, calculate it locally
        commitment = stored_commitment if stored_commitment else self._generate_commitment(key_value, nullifier)
        
        # Generate the proof
        logger.debug("Client-side proof calculation:")
        logger.debug(f"Nullifier: {nullifier}")
        logger.debug(f"Challenge: {challenge}")
        logger.debug(f"Commitment: {commitment}")
        proof = self._generate_proof(nullifier, challenge, commitment)
        
        # Send verification request to server
        verify_url = self._get_zkp_url("/api/v1/verifyProof")
        logger.debug(f"Using URL for verify proof: {verify_url}")
        
        try:
            data = {
                "userId": user_id_to_use,
                "keyName": key_name,
                "proof": proof,
                "nullifier": nullifier,
                "challenge": challenge,
                "clientCommitment": stored_commitment if stored_commitment else "not provided"
            }
            
            logger.debug(f"Sending verification request to: {verify_url}")
            logger.debug(f"Request data: {data}")
            
            response = requests.post(verify_url, json=data, headers=headers)
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response text: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                # If the server always returns verified=true, perform a local verification
                if result.get("verified", False) and key_value:
                    # For local verification, we need to check if the proof matches what we'd expect
                    # If we have a stored commitment, we can verify against it
                    # If not, we can only trust the server's response
                    if stored_commitment and stored_commitment != commitment:
                        # If we got a commitment from the server but it doesn't match our calculated one,
                        # something is wrong - the verification should fail
                        return {
                            "status": "success",
                            "success": True,
                            "verified": False,
                            "error": "Stored commitment doesn't match calculated commitment"
                        }
                
                return {
                    "status": "success",
                    "success": True,
                    "verified": result.get("verified", False)
                }
            elif response.status_code == 402:
                return {"status": "error", "success": False, "error": "Insufficient credits"}
            elif response.status_code == 401 or response.status_code == 403:
                return {"status": "error", "success": False, "error": "Authentication failed"}
            else:
                return {"status": "error", "success": False, "error": f"Unknown error: {response.status_code} - {response.text}"}
        except Exception as e:
            return {"status": "error", "success": False, "error": str(e), "type": type(e).__name__}
    
    # =========================
    # Credit System Methods
    # =========================
    
    def get_user_credits(self, user_id):
        """
        Get the current credit balance for a user.
        
        Args:
            user_id (str): The user's ID
            
        Returns:
            dict: Response containing credit information or error
        """
        # Ensure user is authenticated
        if not self._ensure_authenticated():
            return {
                "success": False,
                "error": "Authentication required. Please provide valid credentials."
            }
            
        url = self._get_zkp_url(f"/v1/mesh/users/{user_id}/credits")
        headers = self._get_headers()
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "success": False,
                    "error": f"Failed to get user credits: {response.status_code}",
                    "details": response.json() if response.content else None
                }
        except requests.RequestException as e:
            return {
                "success": False,
                "error": f"Request failed: {str(e)}"
            }
    
    def ensure_user_exists(self, user_id, email=None):
        """
        Ensure the user exists in the system. If not, creates the user with default credits.
        
        Args:
            user_id (str): The user's ID
            email (str, optional): The user's email
            
        Returns:
            dict: Response containing user information or error
        """
        url = self._get_zkp_url("/v1/mesh/users")
        data = {"id": user_id}
        if email:
            data["email"] = email
        
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "success": False,
                "error": f"Failed to ensure user exists: {response.status_code}",
                "details": response.json() if response.content else None
            }
    
    # =========================
    # Chat Completion Methods
    # =========================
    
    def _normalize_model_name(self, model: str) -> str:
        """Normalize model names to their canonical versions
        
        Args:
            model: The model name to normalize
            
        Returns:
            str: The normalized model name
        """
        if not model:
            return None
            
        # Convert to lowercase and remove any extra whitespace
        model_lower = model.lower().strip()
        
        # Check aliases first
        if model_lower in MODEL_ALIASES:
            return MODEL_ALIASES[model_lower]
            
        # If no alias found, return the original model name
        return model
    
    def _get_provider_for_model(self, model: str) -> str:
        """Determine the provider for a given model
        
        Args:
            model: The model name
            
        Returns:
            str: The provider name ('openai' or 'anthropic')
        """
        if model is None:
            return get_default_provider()
            
        model_lower = model.lower()
        
        # First check if model is in MODEL_ALIASES and determine provider from the canonical name
        if model_lower in MODEL_ALIASES:
            canonical_model = MODEL_ALIASES[model_lower]
            if 'claude' in canonical_model:
                return 'anthropic'
            elif any(name in canonical_model for name in ['gpt', 'text-', 'davinci', 'babbage', 'o1', 'o3']):
                return 'openai'
        
        # Direct check for provider-specific keywords
        if 'claude' in model_lower:
            return 'anthropic'
        elif any(name in model_lower for name in ['gpt', 'text-', 'davinci', 'babbage', 'o1', 'o3']):
            return 'openai'
        
        # Check if model is in PROVIDER_MODELS
        for provider, models in PROVIDER_MODELS.items():
            if model in models:
                return provider
        
        # Default to configured default provider
        return get_default_provider()
    
    def _extract_content_string(self, response: Dict[str, Any]) -> str:
        """Extract the text content from a response in a consistent way
        
        Handles different response formats from different providers
        
        Args:
            response: The API response
            
        Returns:
            str: The extracted text content
        """
        # Handle OpenAI format
        if "choices" in response and len(response["choices"]) > 0:
            if "message" in response["choices"][0]:
                return response["choices"][0]["message"].get("content", "")
            elif "text" in response["choices"][0]:
                return response["choices"][0].get("text", "")
        
        # Handle Anthropic format
        if "content" in response:
            content = response["content"]
            if isinstance(content, list) and len(content) > 0:
                return content[0].get("text", "")
            elif isinstance(content, str):
                return content
        
        # Fallback
        return ""

    def _extract_content(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Extract content from a response in a consistent way
        
        Handles different response formats from different providers
        
        Args:
            response: The API response
            
        Returns:
            dict: The extracted content with text and thinking
        """
        result = {
            "content": "",
            "thinking": None,
            "redacted_thinking": None,
            "raw_response": response
        }
        
        # Handle Anthropic format with thinking blocks
        if "content" in response and isinstance(response["content"], list):
            for block in response["content"]:
                if block.get("type") == "text":
                    result["content"] = block.get("text", "")
                elif block.get("type") == "thinking":
                    result["thinking"] = {
                        "content": block.get("thinking", ""),
                        "signature": block.get("signature", "")
                    }
                elif block.get("type") == "redacted_thinking":
                    result["redacted_thinking"] = {
                        "data": block.get("data", "")
                    }
        else:
            # Use existing content extraction for other formats
            result["content"] = self._extract_content_string(response)
        
        return result

    def _ensure_user_registered(self) -> bool:
        """
        Ensures the user is registered in the database by calling the profile endpoint.
        This is necessary before making chat requests since the chat endpoints
        require the user to exist in the database.
        
        Returns:
            bool: True if the user is registered or successfully registered, False otherwise
        """
        if self._profile_checked:
            # Already checked this session
            return True
            
        # First ensure we have authentication
        if not self._ensure_authenticated():
            return False
            
        try:
            logger.info("Checking user profile to ensure registration")
            
            # Try the new endpoint first with auto-refreshing request
            response = self._request(
                method="GET",
                url=f"{self.mesh_api_url}/api/v1/auth/profile",
                headers=self._get_headers()
            )
            
            if response.status_code == 404:
                # Try the legacy endpoint with auto-refreshing request
                response = self._request(
                    method="GET",
                    url=f"{self.mesh_api_url}/v1/mesh/auth/profile",
                    headers=self._get_headers()
                )
                
            if response.status_code == 200:
                # Parse the response
                data = response.json()
                self._user_profile = data.get('profile', {})
                logger.info(f"User successfully registered with {self._user_profile.get('credits', 0)} credits")
                self._profile_checked = True
                return True
            else:
                logger.warning(f"Failed to register user: {response.status_code}")
                logger.debug(f"Response: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Error checking user profile: {str(e)}")
            return False

    def chat(self, 
             message: str, 
             model: Optional[str] = None, 
             provider: Optional[str] = None,
             thinking: Optional[bool] = None,
             thinking_budget: Optional[int] = None,
             max_tokens: Optional[int] = None,
             temperature: float = 0.7,
             original_response: Optional[bool] = None,
             **kwargs) -> Dict[str, Any]:
        """Send a chat message to an AI model
        
        Args:
            message: The message to send
            model: The model to use (e.g. "gpt-4", "claude-3-7-sonnet")
            provider: The provider to use (e.g. "openai", "anthropic")
            thinking: Whether to enable extended thinking mode (Claude 3.7 Sonnet only)
            thinking_budget: Maximum tokens for thinking (min 1024, must be < max_tokens)
            max_tokens: Maximum number of tokens to generate
            temperature: Temperature for sampling (0.0 to 1.0)
            original_response: Whether to return the original response
            **kwargs: Additional options for the chat request

        Returns:
            dict: The chat response
        """
        # Ensure we're authenticated
        if not self._ensure_authenticated():
            return {
                "success": False,
                "error": "Authentication failed",
                "details": "Could not authenticate with Auth0. Try running 'mesh-auth' from the command line to authenticate manually."
            }
        
        # Make sure the user is registered in the database
        if not self._profile_checked and not self._ensure_user_registered():
            return {
                "success": False,
                "error": "Failed to register user. Chat requires user registration.",
                "troubleshooting": [
                    "Try calling the auth profile endpoint directly first",
                    "Verify your authentication token is valid",
                    "Check that the server URL is correct"
                ]
            }
        
        # Check if model is a Claude model and set provider accordingly
        if model and 'claude' in model.lower():
            provider = 'anthropic'
            logger.debug(f"Detected Claude model, setting provider to anthropic")
        
        # Determine provider if not specified
        if provider is None:
            provider = get_default_provider()
        
        # Set default model if none provided, based on provider (with override support)
        if model is None:
            model = get_default_model_with_override(provider)
            logger.info(f"Using default model for {provider}: {model}")
        
        # Normalize the model name
        model = self._normalize_model_name(model)
        
        # Prepare the request based on the provider
        logger.info(f"Chat: {message[:30]}... using {provider}/{model}")
        
        # Create request data
        request_data = {
            "prompt": message,  # Keep for completions endpoint
            "provider": provider,
            "model": model,
            # Format as OpenAI-compatible messages array for chat/completions endpoint
            "messages": [
                {"role": "user", "content": message}
            ]
        }
        
        # Add thinking mode if enabled
        if thinking:
            request_data["thinking"] = True
            
        # Add thinking budget if specified
        if thinking_budget:
            request_data["thinking_budget"] = thinking_budget
        
        # Add max tokens if specified
        if max_tokens is not None:
            request_data["max_tokens"] = max_tokens
        
        # Add temperature if specified
        if temperature is not None:
            request_data["temperature"] = temperature
        
        # Add any additional parameters
        for key, value in kwargs.items():
            if key not in request_data:
                request_data[key] = value
        
        # Try different endpoints in order
        endpoints = [
            '/api/v1/chat/completions',
            '/v1/mesh/chat',
            '/v1/chat',
            '/v1/complete',
            '/chat',
            '/complete'
        ]
        
        last_error = None
        for endpoint in endpoints:
            url = self._get_chat_url(endpoint)
            
            try:
                logger.info(f"Trying chat endpoint: {url}")
                
                # Use our new _request method with auto-refresh capability
                response = self._request(
                    method="POST", 
                    url=url, 
                    headers=self._get_headers(), 
                    json_data=request_data
                )
                
                logger.info(f"Response status: {response.status_code}")
                
                # Check if request was successful
                if response.status_code == 200:
                    data = response.json()
                    
                    # Return the original response if requested
                    if original_response is not None:
                        use_original = original_response
                    else:
                        use_original = self.config['original_response']
                    
                    if use_original:
                        return data
                    
                    # Extract the content from the response
                    content = self._extract_content_string(data)
                    return content
                
                # Note: 401/403 errors are already handled by _request method for token refresh
                # We'll only get here if the refresh failed or we don't have a refresh token
                
                # Provide detailed error message
                error_data = {}
                try:
                    error_data = response.json() if response.text else {}
                except:
                    error_data = {"text": response.text}
                
                error_message = error_data.get('error', f'Request failed with status {response.status_code}')
                logger.debug(f"Endpoint attempt failed: {error_message}")  # Changed from warning to debug
                
                # Special handling for authentication errors
                if response.status_code == 401 or response.status_code == 403:
                    if "jwt malformed" in str(error_data):
                        error_details = "The authentication token is not in the correct JWT format. Try re-authenticating with 'mesh-auth' command."
                    elif "invalid token" in str(error_data).lower():
                        error_details = "The authentication token is invalid. Try re-authenticating with 'mesh-auth' command."
                    elif "expired" in str(error_data).lower():
                        error_details = "The authentication token has expired. Try re-authenticating with 'mesh-auth' command."
                    else:
                        error_details = error_data
                    
                    last_error = {
                        "success": False,
                        "error": f"Authentication failed: {response.status_code}",
                        "details": {
                            "error": error_message,
                            "help": "Run 'mesh-auth' to authenticate manually",
                            "details": error_details
                        },
                        "url": url
                    }
                else:
                    last_error = {
                        "success": False,
                        "error": f"Request failed: {response.status_code}",
                        "details": error_data,
                        "url": url
                    }

            except requests.RequestException as e:
                # Request exception, try next endpoint
                last_error = {
                    "exception": str(e),
                    "url": url
                }
        
        # If we get here, all endpoints failed
        logger.error("All chat endpoints failed")
        
        # All attempts failed, return error
        return {
            "success": False,
            "error": "Request failed: All endpoints failed",
            "details": last_error,
            "help": "Make sure the server is running and accessible"
        }

    def get_usage(self) -> Dict[str, Any]:
        """
        Get usage data for the authenticated user.
        
        Returns:
            Dict[str, Any]: Usage data
        """
        # Ensure we're authenticated
        if not self._ensure_authenticated():
            return {"success": False, "error": "Not authenticated", "help": "Run 'mesh-auth' to authenticate"}
        
        # Make request to get usage data
        try:
            url = self._get_chat_url('/api/v1/usage')
            response = self._request(
                method="GET", 
                url=url, 
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                error_data = {}
                try:
                    error_data = response.json() if response.text else {}
                except:
                    error_data = {"text": response.text}
                
                return {
                    "success": False,
                    "error": f"Failed to get usage data: {response.status_code}",
                    "details": error_data
                }
        except Exception as e:
            return {
                "success": False,
                "error": f"Exception while getting usage data: {str(e)}"
            }
            
    def get_models(self) -> Dict[str, Any]:
        """
        Get available models grouped by provider.
        
        Returns:
            Dict[str, Any]: Available models by provider
        """
        # Ensure we're authenticated
        if not self._ensure_authenticated():
            return {"success": False, "error": "Not authenticated", "help": "Run 'mesh-auth' to authenticate"}
        
        # First try to get models from the server
        try:
            url = self._get_chat_url('/api/v1/models')
            response = self._request(
                method="GET", 
                url=url, 
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.debug(f"Could not fetch models from server: {str(e)}")
        
        # If server doesn't provide models, return a curated list based on known models
        models = {
            "success": True,
            "models": {
                "openai": [
                    "gpt-4o",
                    "gpt-4o-2024-08-06",
                    "gpt-4",
                    "gpt-4-turbo",
                    "gpt-3.5-turbo"
                ],
                "anthropic": [
                    "claude-3-opus-20240229",
                    "claude-3-sonnet-20240229",
                    "claude-3-haiku-20240307",
                    "claude-3-5-sonnet-20240620",
                    "claude-3-7-sonnet"
                ]
            }
        }
        
        # Add information about which models are available based on usage history
        usage_data = self.get_usage()
        available_models = {}
        
        if usage_data.get("success", False):
            # Check if the data is in the new format
            if "data" in usage_data:
                for entry in usage_data["data"]:
                    if "service" in entry and "action" in entry:
                        provider = entry["service"]
                        model_name = entry["action"]
                        
                        # Also check metadata for model info
                        if "metadata" in entry and "model" in entry["metadata"]:
                            model_name = entry["metadata"]["model"]
                        
                        if provider not in available_models:
                            available_models[provider] = set()
                        
                        available_models[provider].add(model_name)
            # Check if the data is in the old format
            elif "usage" in usage_data:
                for entry in usage_data["usage"]:
                    if "service" in entry and "model" in entry:
                        provider = entry["service"]
                        model_name = entry["model"]
                        
                        if provider not in available_models:
                            available_models[provider] = set()
                        
                        available_models[provider].add(model_name)
        
        # Convert sets to lists for JSON serialization
        for provider in available_models:
            available_models[provider] = list(available_models[provider])
        
        models["available_models"] = available_models
        
        return models
        
    def chat_with_gpt4o(self, message: str, **kwargs) -> Dict[str, Any]:
        """Chat with GPT-4o
        
        Args:
            message: The message to send
            **kwargs: Additional options for the chat request
            
        Returns:
            dict: The chat response
        """
        return self.chat(message, model="gpt-4o", provider="openai", **kwargs)
    
    def chat_with_gpt4(self, message: str, **kwargs) -> Dict[str, Any]:
        """Chat with GPT-4
        
        Args:
            message: The message to send
            **kwargs: Additional options for the chat request
            
        Returns:
            dict: The chat response
        """
        return self.chat(message, model="gpt-4", provider="openai", **kwargs)
    
    def chat_with_claude(self, message: str, version: str = "3.5", **kwargs) -> Dict[str, Any]:
        """Chat with Claude
        
        Args:
            message: The message to send
            version: Claude version to use: "3.5" (default), "3.7", or "3"
            **kwargs: Additional options for the chat request
            
        Returns:
            dict: The chat response
        """
        # Map version string to actual model
        if version == "3.7":
            model = "claude-3-7-sonnet-20250219"
        elif version == "3":
            model = "claude-3-opus-20240229"
        else:  # Default to 3.5
            model = "claude-3-5-sonnet-20241022"
        
        return self.chat(message, model=model, provider="anthropic", **kwargs)
    
    def chat_with_best_model(self, message: str, provider: str = None, **kwargs) -> Dict[str, Any]:
        """Chat with the best model for a provider
        
        Args:
            message: The message to send
            provider: The provider to use (default: from configuration)
            **kwargs: Additional options for the chat request
            
        Returns:
            dict: The chat response
        """
        from .models import get_best_model
        
        provider = provider or get_default_provider()
        model = get_best_model(provider)
        
        return self.chat(message, model=model, provider=provider, **kwargs)
    
    def chat_with_fastest_model(self, message: str, provider: str = None, **kwargs) -> Dict[str, Any]:
        """Chat with the fastest model for a provider
        
        Args:
            message: The message to send
            provider: The provider to use (default: from configuration)
            **kwargs: Additional options for the chat request
            
        Returns:
            dict: The chat response
        """
        from .models import get_fastest_model
        
        provider = provider or get_default_provider()
        model = get_fastest_model(provider)
        
        return self.chat(message, model=model, provider=provider, **kwargs)
    
    def chat_with_cheapest_model(self, message: str, provider: str = None, **kwargs) -> Dict[str, Any]:
        """Chat with the cheapest model for a provider
        
        Args:
            message: The message to send
            provider: The provider to use (default: from configuration)
            **kwargs: Additional options for the chat request
            
        Returns:
            dict: The chat response
        """
        from .models import get_cheapest_model
        
        provider = provider or get_default_provider()
        model = get_cheapest_model(provider)
        
        return self.chat(message, model=model, provider=provider, **kwargs)

    def chat_with_thinking(self, message: str, thinking_budget: Optional[int] = None, max_tokens: Optional[int] = None, **kwargs) -> Dict[str, Any]:
        """Chat with Claude 3.7 Sonnet using extended thinking
        
        Args:
            message: The message to send
            thinking_budget: Maximum tokens for thinking (min 1024, default 4000)
            max_tokens: Maximum number of tokens to generate
            **kwargs: Additional options for the chat request
            
        Returns:
            dict: The chat response with thinking content
        """
        # Import here to avoid circular imports
        from .models import Anthropic
        
        return self.chat(
            message, 
            model=Anthropic.CLAUDE_3_7_SONNET, 
            provider="anthropic", 
            thinking=True,
            thinking_budget=thinking_budget,
            max_tokens=max_tokens,
            **kwargs
        )

    def chat_with_small_thinking(self, message: str, **kwargs) -> Dict[str, Any]:
        """Chat with Claude 3.7 Sonnet using a small thinking budget (2000 tokens)
        
        Args:
            message: The message to send
            **kwargs: Additional options for the chat request
            
        Returns:
            dict: The chat response with thinking content
        """
        # Import here to avoid circular imports
        from .models import Anthropic
        
        return self.chat(
            message, 
            model=Anthropic.CLAUDE_3_7_SONNET,
            provider="anthropic",
            thinking=True,
            thinking_budget=2000,
            **kwargs
        )

    def chat_with_medium_thinking(self, message: str, **kwargs) -> Dict[str, Any]:
        """Chat with Claude 3.7 Sonnet using a medium thinking budget (8000 tokens)
        
        Args:
            message: The message to send
            **kwargs: Additional options for the chat request
            
        Returns:
            dict: The chat response with thinking content
        """
        # Import here to avoid circular imports
        from .models import Anthropic
        
        return self.chat(
            message, 
            model=Anthropic.CLAUDE_3_7_SONNET,
            provider="anthropic",
            thinking=True,
            thinking_budget=8000,
            **kwargs
        )

    def chat_with_large_thinking(self, message: str, **kwargs) -> Dict[str, Any]:
        """Chat with Claude 3.7 Sonnet using a large thinking budget (16000 tokens)
        
        Args:
            message: The message to send
            **kwargs: Additional options for the chat request
            
        Returns:
            dict: The chat response with thinking content
        """
        # Import here to avoid circular imports
        from .models import Anthropic
        
        # Set max_tokens to 32000 to ensure it's larger than the thinking budget
        return self.chat(
            message, 
            model=Anthropic.CLAUDE_3_7_SONNET,
            provider="anthropic",
            thinking=True,
            thinking_budget=16000,
            max_tokens=32000,
            **kwargs
        )

    def set_default_model(self, provider: str, model: str) -> None:
        """Set the default model for a provider
        
        This setting persists only for the current session.
        
        Args:
            provider: The provider name (e.g., "openai", "anthropic")
            model: The model name to use as default
        """
        provider = provider.lower()
        
        if provider == "openai":
            os.environ["DEFAULT_OPENAI_MODEL_OVERRIDE"] = model
            logger.info(f"Set default OpenAI model to: {model}")
        elif provider == "anthropic":
            os.environ["DEFAULT_ANTHROPIC_MODEL_OVERRIDE"] = model
            logger.info(f"Set default Anthropic model to: {model}")
        else:
            logger.warning(f"Unknown provider: {provider}")

    def reset_default_models(self) -> None:
        """Reset all default model overrides to their original values"""
        os.environ.pop("DEFAULT_OPENAI_MODEL_OVERRIDE", None)
        os.environ.pop("DEFAULT_ANTHROPIC_MODEL_OVERRIDE", None)
        logger.info("Reset all default model overrides")

    # Helper methods for token persistence - keeping these for backward compatibility
    def _load_token_from_disk(self) -> Optional[str]:
        """Load token using token_manager - kept for backward compatibility"""
        # First try token manager
        self._load_token()
        if self._auth_token:
            return self._auth_token
            
        # Then fall back to old method for backward compatibility
        import json
        path = os.path.expanduser('~/.mesh/auth.json')
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    token = data.get('auth_token')
                    if token:
                        # If we found a token in the old location, store it properly
                        # in the token manager for future use
                        self.auth_token = token
                        return token
            except Exception as e:
                logger.warning(f"Failed to load token from disk: {e}")
        return None

    def _save_token_to_disk(self, token: str) -> None:
        """Save token using token_manager - kept for backward compatibility"""
        # Save to token manager
        self.auth_token = token
        
        # Also save to old location for backward compatibility
        import json
        dir_path = os.path.expanduser('~/.mesh')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        path = os.path.join(dir_path, 'auth.json')
        try:
            with open(path, 'w') as f:
                json.dump({'auth_token': token}, f)
        except Exception as e:
            logger.warning(f"Failed to save token to disk: {e}")

    def _request_with_retry(self, method, url, data=None, headers=None, json_data=None, max_retries=3):
        """Make request with comprehensive authentication handling and retry mechanism
        
        This method handles all authentication scenarios and retries:
        - Auto refresh of expired tokens
        - Automatic retries on network issues
        - Full authentication recovery
        
        Args:
            method (str): HTTP method
            url (str): Request URL
            data: Request data
            headers (dict): Request headers
            json_data: JSON data
            max_retries (int): Maximum retry attempts
            
        Returns:
            Response: Response object
        """
        retry_count = 0
        backoff = 1.0
        
        while retry_count <= max_retries:
            try:
                # Ensure authentication before request
                if not self._ensure_authenticated():
                    raise Exception("Could not authenticate after exhausting all methods")
                
                # Update headers with current token
                if headers is None:
                    headers = {}
                headers["Authorization"] = f"Bearer {self._auth_token}"
                
                # Make request
                response = requests.request(
                    method=method,
                    url=url,
                    data=data,
                    headers=headers,
                    json=json_data,
                    timeout=30
                )
                
                # If unauthorized, try to reauthenticate and retry
                if response.status_code in [401, 403]:
                    if retry_count < max_retries:
                        logger.info(f"Received {response.status_code}, attempting recovery (attempt {retry_count+1})")
                        # Clear token to force full reauthentication
                        self._auth_token = None
                        if not self._ensure_authenticated():
                            raise Exception("Authentication recovery failed")
                        retry_count += 1
                        continue
                
                return response
                
            except requests.RequestException as e:
                # Network error handling with exponential backoff
                if retry_count < max_retries:
                    logger.warning(f"Request error: {str(e)}, retrying in {backoff} seconds")
                    time.sleep(backoff)
                    backoff *= 2
                    retry_count += 1
                    continue
                else:
                    logger.error(f"Request failed after {max_retries} attempts: {str(e)}")
                    raise
        
        raise Exception(f"Request failed after {max_retries} attempts")

    def _request(self, method, url, data=None, headers=None, json_data=None, use_retry=True):
        """Make a request, optionally with retries and automatic authentication
        
        Args:
            method (str): HTTP method
            url (str): Request URL
            data: Request data
            headers (dict): Request headers
            json_data: JSON data
            use_retry (bool): Whether to use retry mechanism
            
        Returns:
            Response: Response object
        """
        # If retry mechanism is enabled, use it
        if use_retry:
            return self._request_with_retry(method, url, data, headers, json_data)
        
        # Otherwise, use original request mechanism
        if self._auth_token:
            if headers is None:
                headers = {}
            headers["Authorization"] = f"Bearer {self._auth_token}"
        
        response = requests.request(
            method=method,
            url=url,
            data=data,
            headers=headers,
            json=json_data,
            timeout=30
        )
        
        # Handle authentication errors
        if response.status_code == 401 and self.auto_refresh and self._token_data and "refresh_token" in self._token_data:
            logger.info("Received 401 response, attempting to refresh token")
            refresh_success = self._refresh_token_with_retry()
            
            # If refresh succeeded, retry the request with new token
            if refresh_success:
                logger.info("Token refreshed, retrying request")
                
                # Update authorization header with new token
                if headers is None:
                    headers = {}
                headers["Authorization"] = f"Bearer {self._auth_token}"
                
                # Retry request
                response = requests.request(
                    method=method,
                    url=url,
                    data=data,
                    headers=headers,
                    json=json_data,
                    timeout=30
                )
        
        return response

    def _make_api_request(self, endpoint: str, method: str = "POST", url_base: str = None, data: Dict = None, 
                         additional_headers: Dict = None, timeout: int = 60) -> Dict[str, Any]:
        """Make an API request with error handling
        
        Args:
            endpoint: API endpoint path
            method: HTTP method (GET, POST, etc.)
            url_base: Base URL to use, defaults to server URL
            data: Data to send in the request
            additional_headers: Additional headers to include
            timeout: Request timeout in seconds
            
        Returns:
            dict: Parsed response data
        """
        # Choose the right base URL
        url_base = url_base or self.server_url
        
        # Build the URL
        url = f"{url_base}{endpoint}"
        
        # Get headers with authentication
        headers = self._get_headers(additional_headers)
        
        try:
            # Make the request with retry logic
            response = self._request(
                method=method,
                url=url,
                json_data=data,
                headers=headers,
                timeout=timeout
            )
            
            # Parse and return the response
            try:
                response_data = response.json()
            except ValueError:
                response_data = {"text": response.text}
            
            # Add status code to response data
            response_data["status_code"] = response.status_code
            
            # Handle error status codes
            if response.status_code >= 400:
                error_message = response_data.get("error", {}).get("message", response_data.get("error", "Unknown error"))
                logger.error(f"API request failed: {error_message}")
                response_data["error"] = error_message
            
            return response_data
        except Exception as e:
            logger.error(f"API request failed with exception: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "status_code": 500
            } 

    def _verify_token_integrity(self):
        """Verify the integrity of the stored token
        
        Returns:
            bool: True if token integrity check passed
        """
        if not self._token_data:
            return False
        
        # If token has integrity hash, verify it
        if "_integrity_hash" in self._token_data:
            try:
                # Create copy without the hash
                token_copy = self._token_data.copy()
                stored_hash = token_copy.pop("_integrity_hash")
                
                # Check if the stored timestamp is reasonable (not too old)
                stored_at = token_copy.get("_stored_at", 0)
                if time.time() - stored_at > 90 * 24 * 60 * 60:  # 90 days
                    logger.warning("Token data is very old (>90 days), might be stale")
                
                # Calculate hash for comparison
                import hashlib
                token_json = json.dumps(token_copy, sort_keys=True)
                calculated_hash = hashlib.sha256(token_json.encode()).hexdigest()
                
                # Compare hashes
                if calculated_hash != stored_hash:
                    logger.warning("Token integrity check failed - token data may be corrupted")
                    return False
                
                logger.debug("Token integrity check passed")
                return True
            except Exception as e:
                logger.warning(f"Token integrity check error: {str(e)}")
                return False
        
        # No integrity hash present
        return True

    def _start_token_health_monitor(self):
        """Start background thread to monitor token health
        
        This ensures tokens are refreshed before they expire.
        """
        def monitor_token():
            import random
            import threading
            
            while True:
                try:
                    # Check if token will expire in the next 10 minutes
                    if self._token_data and "expires_at" in self._token_data:
                        expires_at = self._token_data["expires_at"]
                        now = time.time()
                        
                        # If token expires in less than 10 minutes, refresh it
                        if expires_at - now < 600:
                            logger.info("Token expiring soon, preemptively refreshing")
                            self._refresh_token_with_retry()
                    
                    # Only verify token integrity once per hour
                    if random.random() < 0.01:  # 1% chance each check
                        self._verify_token_integrity()
                except Exception as e:
                    logger.warning(f"Token health monitor error: {str(e)}")
                
                # Check every minute
                time.sleep(60)
        
        # Start thread
        import threading
        thread = threading.Thread(target=monitor_token, daemon=True)
        thread.start()
        logger.info("Token health monitor started")

    # =========================
    # Key Management Methods
    # =========================

    def list_keys(self, user_id: Optional[str] = None) -> List[str]:
        """List all keys stored for a user
        
        Args:
            user_id: Optional User ID to list keys for. If not provided, extracted from auth token.
            
        Returns:
            List[str]: A list of key names (without the user_id prefix)
        """
        # Ensure we're authenticated
        if not self._ensure_authenticated():
            logger.error("Authentication failed")
            return []
        
        # Get user profile to extract user ID if not provided
        if not user_id:
            if not self._user_profile:
                self._ensure_user_registered()
            
            if self._user_profile and 'id' in self._user_profile:
                user_id = self._user_profile.get('id')
                logger.info(f"Using user ID from profile: {user_id}")
            else:
                logger.error("Could not determine user ID")
                return []
        
        # Make the request to list keys
        url = self._get_zkp_url("/api/v1/listKeys")
        headers = self._get_headers()
        
        try:
            response = requests.get(
                url,
                headers=headers,
                params={"userId": user_id}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Return empty list if request failed
                if not result.get("success"):
                    logger.warning(f"Key listing failed: {result.get('error', 'Unknown error')}")
                    return []
                
                # Return the list of keys
                keys = result.get("keys", [])
                logger.info(f"Successfully retrieved {len(keys)} keys for user: {user_id}")
                return keys
            else:
                logger.error(f"Failed to list keys: {response.status_code}")
                return []
            
        except requests.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            return []