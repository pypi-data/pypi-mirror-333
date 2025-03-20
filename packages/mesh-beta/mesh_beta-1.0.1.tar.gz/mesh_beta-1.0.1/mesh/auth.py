"""
Authentication Module for Mesh SDK

This module handles authentication with Auth0, including browser-based login
and device code flow for headless environments.
"""

import os
import sys
import time
import json
import logging
import webbrowser
import socketserver
import http.server
import threading
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
    get_token_exchange_endpoint
)

# Configure logging
logger = logging.getLogger("mesh.auth")

# Get configuration - these will be populated from the backend when needed
AUTH0_DOMAIN = get_config("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = get_config("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = get_config("AUTH0_CLIENT_SECRET")
AUTH0_AUDIENCE = get_config("AUTH0_AUDIENCE")

# Create a cache for Auth0 configuration
AUTH0_CONFIG_CACHE = {}

def get_auth0_config() -> Dict[str, str]:
    """
    Get Auth0 configuration from the backend.
    
    Returns:
        Dict[str, str]: Auth0 configuration including domain, client_id, and audience
    """
    global AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_AUDIENCE, AUTH0_CONFIG_CACHE
    
    # Return cached config if available and not empty
    if AUTH0_CONFIG_CACHE and all(AUTH0_CONFIG_CACHE.values()):
        return AUTH0_CONFIG_CACHE
    
    # If environment variables are set, use those
    if all([
        get_config("AUTH0_DOMAIN"), 
        get_config("AUTH0_CLIENT_ID"),
        get_config("AUTH0_CLIENT_SECRET"),
        get_config("AUTH0_AUDIENCE")
    ]):
        AUTH0_CONFIG_CACHE = {
            "domain": get_config("AUTH0_DOMAIN"),
            "client_id": get_config("AUTH0_CLIENT_ID"),
            "client_secret": get_config("AUTH0_CLIENT_SECRET"),
            "audience": get_config("AUTH0_AUDIENCE")
        }
        return AUTH0_CONFIG_CACHE
    
    try:
        # Fetch Auth0 configuration from the backend
        response = requests.get(get_auth_config_endpoint())
        response.raise_for_status()
        
        config = response.json()
        if config and "domain" in config and "client_id" in config:
            # Update global variables
            AUTH0_DOMAIN = config.get("domain", "")
            AUTH0_CLIENT_ID = config.get("client_id", "")
            AUTH0_CLIENT_SECRET = config.get("client_secret", "")
            AUTH0_AUDIENCE = config.get("audience", "")
            
            # Update cache
            AUTH0_CONFIG_CACHE = config
            return config
        else:
            logger.error("Invalid Auth0 configuration received from backend")
            return {}
    except Exception as e:
        logger.error(f"Failed to fetch Auth0 configuration from backend: {str(e)}")
        return {}

class CallbackHandler(http.server.BaseHTTPRequestHandler):
    """Handler for OAuth callback"""
    
    # Class variables to store state
    token_data = None
    server_ready = None  # Will be set to a threading.Event()
    
    def do_GET(self):
        """Handle GET request - capture the auth code and exchange it for a token"""
        if "/callback" in self.path:
            # Get query parameters
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            
            # Check for error
            if "error" in params:
                error = params["error"][0]
                error_description = params.get("error_description", [""])[0]
                
                logger.error(f"Auth0 returned an error: {error} - {error_description}")
                
                # Send error response
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                
                error_html = f"""
                <html>
                <head><title>Authentication Error</title></head>
                <body>
                <h1>Authentication Error</h1>
                <p>{error}: {error_description}</p>
                <p>Please close this window and try again.</p>
                </body>
                </html>
                """
                
                self.wfile.write(error_html.encode())
                
                # Signal that we're done, but with failure
                if CallbackHandler.server_ready:
                    CallbackHandler.server_ready.set()
                    return
            
            # Check for authorization code
            if "code" in params:
                code = params["code"][0]
                state = params.get("state", [""])[0]
                
                logger.info(f"Received authorization code, state: {state}")
                
                # Use backend token exchange endpoint instead of direct Auth0 call
                try:
                    # Exchange code for token
                    token_data = exchange_code_for_token(code)
                    
                    if token_data and "access_token" in token_data:
                        # Store token data in class variable
                        CallbackHandler.token_data = token_data
                        
                        # Store token securely
                        store_token(token_data)
                        
                        # Send success response
                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        
                        success_html = """
                        <html>
                        <head><title>Authentication Successful</title></head>
                        <body>
                        <h1>Authentication Successful</h1>
                        <p>You have been successfully authenticated.</p>
                        <p>You can close this window now.</p>
                        <script>window.close();</script>
                        </body>
                        </html>
                        """
                        
                        self.wfile.write(success_html.encode())
                    else:
                        # Send error response
                        self.send_response(400)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        
                        error_html = """
                        <html>
                        <head><title>Authentication Error</title></head>
                        <body>
                        <h1>Authentication Error</h1>
                        <p>Failed to exchange code for token.</p>
                        <p>Please close this window and try again.</p>
                        </body>
                        </html>
                        """
                        
                        self.wfile.write(error_html.encode())
                except Exception as e:
                    logger.error(f"Error exchanging code for token: {str(e)}")
                    
                    # Send error response
                    self.send_response(500)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    
                    error_html = f"""
                    <html>
                    <head><title>Authentication Error</title></head>
                    <body>
                    <h1>Authentication Error</h1>
                    <p>An error occurred: {str(e)}</p>
                    <p>Please close this window and try again.</p>
                    </body>
                    </html>
                    """
                    
                    self.wfile.write(error_html.encode())
            else:
                # No code, send error response
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                
                error_html = """
                <html>
                <head><title>Authentication Error</title></head>
                <body>
                <h1>Authentication Error</h1>
                <p>No authorization code received.</p>
                <p>Please close this window and try again.</p>
                </body>
                </html>
                """
                
                self.wfile.write(error_html.encode())
            
            # Signal that we're done
            if CallbackHandler.server_ready:
                CallbackHandler.server_ready.set()
        else:
            # Not a callback, send 404
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            not_found_html = """
            <html>
            <head><title>404 Not Found</title></head>
            <body>
            <h1>404 Not Found</h1>
            </body>
            </html>
            """
            
            self.wfile.write(not_found_html.encode())
    
    def log_message(self, format, *args):
        """Override to disable request logging"""
        pass

def exchange_code_for_token(code: str) -> Dict[str, Any]:
    """
    Exchange authorization code for token using the backend.
    
    Args:
        code: Authorization code from Auth0
        
    Returns:
        dict: Token data or empty dict if exchange failed
    """
    try:
        # Use the backend token exchange endpoint
        exchange_url = get_token_exchange_endpoint()
        
        # Prepare data for token exchange
        exchange_data = {
                "code": code,
            "redirect_uri": f"http://localhost:{get_config('AUTH0_CALLBACK_PORT', '8000')}/callback"
        }
        
        # Make request to backend
        response = requests.post(exchange_url, json=exchange_data)
        response.raise_for_status()
        
        token_data = response.json()
        if not token_data or "access_token" not in token_data:
            logger.error("No access token in token exchange response")
            return {}
        
        # Calculate token expiration time if not provided
        if "expires_in" in token_data and "expires_at" not in token_data:
            token_data["expires_at"] = time.time() + token_data["expires_in"]
        
        return token_data
    except Exception as e:
        logger.error(f"Error exchanging code for token: {str(e)}")
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

def authenticate_browser(
    domain: str = None,
    client_id: str = None,
    client_secret: str = None,
    audience: str = None,
    port: int = 8000,
    timeout: int = 300
) -> Dict[str, Any]:
    """
    Authenticate using browser-based flow.
    
    This function starts a local server to handle the OAuth callback,
    then opens a browser for the user to authenticate with Auth0.
    
    Args:
        domain: Auth0 domain
        client_id: Auth0 client ID
        client_secret: Auth0 client secret
        audience: Auth0 audience
        port: Port to use for the callback server
        timeout: Timeout in seconds for the callback server
        
    Returns:
        dict: Token data or None if authentication failed
    """
    # Get Auth0 configuration if not provided
    auth0_config = get_auth0_config()
    
    domain = domain or auth0_config.get("domain") or AUTH0_DOMAIN
    client_id = client_id or auth0_config.get("client_id") or AUTH0_CLIENT_ID
    client_secret = client_secret or auth0_config.get("client_secret") or AUTH0_CLIENT_SECRET
    audience = audience or auth0_config.get("audience") or AUTH0_AUDIENCE
    
    # Check if we have all required configuration
    if not all([domain, client_id, audience]):
        missing = []
        if not domain:
            missing.append("domain")
        if not client_id:
            missing.append("client_id")
        if not audience:
            missing.append("audience")
        
        logger.error(f"Missing required Auth0 configuration: {', '.join(missing)}")
        return None
    
    # Generate a random state value for security
    state = f"auth0_{int(time.time())}"
    
    # Set up the callback handler
    CallbackHandler.token_data = None
    CallbackHandler.server_ready = threading.Event()
    
    # Start the callback server
    try:
        server = socketserver.TCPServer(("localhost", port), CallbackHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        # Wait for server to start
        if not CallbackHandler.server_ready.wait(timeout=5):
            logger.error("Failed to start authentication server")
            return None
        
        logger.info("Auth server started on port %d", port)
    except Exception as e:
        logger.error(f"Failed to start authentication server: {str(e)}")
        return None
    
    try:
        # Get the authorization URL from the backend
        redirect_uri = f"http://localhost:{port}/callback"
        
        # Try to get auth URL from backend first (preferred)
        try:
            auth_url = get_auth_url_from_backend(redirect_uri, state)
            if not auth_url:
                # Fall back to direct Auth0 URL construction
                auth_url = get_auth_url_direct(domain, client_id, redirect_uri, audience, state)
        except Exception as e:
            logger.warning(f"Failed to get auth URL from backend: {str(e)}")
            # Fall back to direct Auth0 URL construction
            auth_url = get_auth_url_direct(domain, client_id, redirect_uri, audience, state)
        
        # Open browser with the authorization URL
        logger.info("Opening browser for authentication")
        webbrowser.open(auth_url)
        
        # Wait for callback with timeout
        logger.info(f"Waiting for authentication to complete (timeout: {timeout} seconds)")
        if not CallbackHandler.server_ready.wait(timeout=timeout):
            logger.error("Authentication timed out")
            return None
        
        # Get token data from handler
        token_data = CallbackHandler.token_data
        
        if token_data and "access_token" in token_data:
            logger.info("Authentication successful")
            
            # Store token and return
            store_token(token_data)
            return token_data
        else:
            logger.error("Authentication failed")
            return None
    finally:
        # Clean up
        server.shutdown()
        server.server_close()
        logger.info("Auth server stopped")

def get_auth_url_from_backend(redirect_uri: str, state: str) -> str:
    """
    Get authorization URL from the backend.
    
    Args:
        redirect_uri: Redirect URI for the callback
        state: State parameter for security
        
    Returns:
        str: Authorization URL
    """
    try:
        response = requests.post(
            get_auth_url_endpoint(),
            json={
                "redirect_uri": redirect_uri,
                "scope": "openid profile email offline_access",
                "state": state
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("auth_url")
        else:
            logger.warning(f"Failed to get auth URL from backend: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.warning(f"Error getting auth URL from backend: {str(e)}")
        return None

def get_auth_url_direct(domain: str, client_id: str, redirect_uri: str, audience: str, state: str) -> str:
    """
    Construct Auth0 authorization URL directly.
    
    Args:
        domain: Auth0 domain
        client_id: Auth0 client ID
        redirect_uri: Redirect URI for the callback
        audience: Auth0 audience
        state: State parameter for security
        
    Returns:
        str: Authorization URL
    """
    auth_url = f"https://{domain}/authorize"
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "openid profile email offline_access",
        "audience": audience,
        "state": state
    }
    
    # Construct the URL with parameters
    auth_url += "?" + "&".join([f"{k}={urllib.parse.quote(v)}" for k, v in params.items()])
    
    return auth_url

def authenticate(
    domain: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    audience: Optional[str] = None,
    port: Optional[int] = None,
    timeout: int = 300,
    headless: bool = False,
    device_flow: bool = False
) -> Dict[str, Any]:
    """
    Perform authentication with Auth0 using either device code flow or browser flow.
    
    This function attempts to authenticate the user. First it checks if there's a
    valid stored token, and if not, it initiates the appropriate authentication flow.
    
    Args:
        domain: Auth0 domain
        client_id: Auth0 client ID
        client_secret: Auth0 client secret
        audience: Auth0 audience
        port: Port to use for the callback server in browser flow
        timeout: Timeout in seconds for the callback server in browser flow
        headless: Whether we are running in a headless environment
        device_flow: Whether to use device code flow regardless of environment
        
    Returns:
        dict: Token data or None if authentication failed
    """
    # Load configuration values if not provided - try to get from backend if needed
    auth0_config = get_auth0_config()
    
    domain = domain or auth0_config.get("domain") or AUTH0_DOMAIN
    client_id = client_id or auth0_config.get("client_id") or AUTH0_CLIENT_ID
    client_secret = client_secret or auth0_config.get("client_secret") or AUTH0_CLIENT_SECRET
    audience = audience or auth0_config.get("audience") or AUTH0_AUDIENCE
    port = port or int(get_config("AUTH0_CALLBACK_PORT", "8000"))
    
    # Check if we have all required configuration
    if not all([domain, client_id, audience]):  # client_secret can be empty for some flows
        missing = []
        if not domain:
            missing.append("domain")
        if not client_id:
            missing.append("client_id")
        if not audience:
            missing.append("audience")
        
        logger.error(f"Missing required Auth0 configuration: {', '.join(missing)}")
        logger.info("The SDK will attempt to continue with backend-driven authentication.")
    
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
    
    # Determine which authentication flow to use
    # If device_flow is explicitly requested, use that
    if device_flow:
        logger.info("Using device code flow as requested")
        return authenticate_device_flow(domain, client_id, client_secret, audience)
    
    # If we're in a headless environment, use device code flow
    if headless or not sys.stdout.isatty() or os.environ.get("CI") or os.environ.get("HEADLESS"):
        logger.info("Detected headless environment, using device code flow")
        return authenticate_device_flow(domain, client_id, client_secret, audience)
    
    # Otherwise, use browser-based flow
    logger.info("Using browser-based authentication flow")
    return authenticate_browser(domain, client_id, client_secret, audience, port, timeout)

def authenticate_device_flow(
    domain: str = None,
    client_id: str = None,
    client_secret: str = None,
    audience: str = None
) -> Dict[str, Any]:
    """
    Authenticate using device code flow.
    
    This function initiates the device code flow, which is suitable for
    headless environments where a browser is not available.
    
    Args:
        domain: Auth0 domain
        client_id: Auth0 client ID
        client_secret: Auth0 client secret
        audience: Auth0 audience
        
    Returns:
        dict: Token data or None if authentication failed
    """
    # Get Auth0 configuration if not provided
    auth0_config = get_auth0_config()
    
    domain = domain or auth0_config.get("domain") or AUTH0_DOMAIN
    client_id = client_id or auth0_config.get("client_id") or AUTH0_CLIENT_ID
    client_secret = client_secret or auth0_config.get("client_secret") or AUTH0_CLIENT_SECRET
    audience = audience or auth0_config.get("audience") or AUTH0_AUDIENCE
    
    # Check if we have all required configuration
    if not all([domain, client_id, audience]):
        missing = []
        if not domain:
            missing.append("domain")
        if not client_id:
            missing.append("client_id")
        if not audience:
            missing.append("audience")
        
        logger.error(f"Missing required Auth0 configuration: {', '.join(missing)}")
        return None
    
    # Define the scope for the device code request
    # Include offline_access to get a refresh token
    scope = "openid profile email offline_access"
    
    logger.debug(f"Device code request with scope: {scope}")
    
    # Request a device code
    try:
        device_code_url = f"https://{domain}/oauth/device/code"
        device_code_data = {
            "client_id": client_id,
            "scope": scope,
            "audience": audience
        }
        
        device_code_response = requests.post(
            device_code_url,
            json=device_code_data,
            headers={"Content-Type": "application/json"}
        )
        
        if device_code_response.status_code != 200:
            logger.error(f"Failed to get device code: {device_code_response.status_code} - {device_code_response.text}")
            return None
        
        device_code_result = device_code_response.json()
        
        # Extract the necessary information
        device_code = device_code_result.get("device_code")
        user_code = device_code_result.get("user_code")
        verification_uri = device_code_result.get("verification_uri")
        verification_uri_complete = device_code_result.get("verification_uri_complete")
        polling_interval = device_code_result.get("interval", 5)
        expires_in = device_code_result.get("expires_in", 900)
        
        # Display instructions to the user
        logger.info("=== Mesh SDK Device Authentication ===")
        logger.info(f"Please visit: {verification_uri}")
        logger.info(f"And enter code: {user_code}")
        logger.info(f"Or visit this URL directly: {verification_uri_complete}")
        
        # Try to open the browser with the verification URL
        try:
            webbrowser.open(verification_uri_complete)
            logger.info("Browser opened with the verification URL.")
        except:
            logger.info("Could not open browser automatically.")
        
        logger.info("Waiting for device authorization...")
        
        # Poll for the token
        token_url = f"https://{domain}/oauth/token"
        token_data = {
            "client_id": client_id,
            "device_code": device_code,
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code"
        }
        
        # Add client_secret if available
        if client_secret:
            token_data["client_secret"] = client_secret
        
        # Poll until we get a token or an error
        start_time = time.time()
        while time.time() - start_time < expires_in:
            # Wait for the polling interval
            time.sleep(polling_interval)
            
            # Request the token
            token_response = requests.post(
                token_url,
                json=token_data,
                headers={"Content-Type": "application/json"}
            )
            
            # Check the response
            if token_response.status_code == 200:
                # Success! We got a token
                token_result = token_response.json()
                
                # Check if we got a refresh token
                if "refresh_token" in token_result:
                    logger.info("Refresh token received")
                else:
                    logger.warning("No refresh token received")
                    logger.warning("To enable refresh tokens, configure your Auth0 application:")
                    logger.warning("   1. Enable 'Refresh Token' grant type in application settings")
                    logger.warning("   2. Enable 'Allow Offline Access' for the API")
                
                # Add expires_at for convenience
                if "expires_in" in token_result:
                    token_result["expires_at"] = int(time.time()) + token_result["expires_in"]
                
                # Store the token
                store_token(token_result)
                
                logger.info("Authentication successful! You can now use the Mesh SDK.")
                return token_result
            elif token_response.status_code == 400:
                # Check the error
                error_data = token_response.json()
                error = error_data.get("error", "")
                
                if error == "authorization_pending":
                    # Still waiting for the user to authorize
                    logger.debug(".", end="", flush=True)
                    continue
                elif error == "slow_down":
                    # We're polling too fast, increase the interval
                    polling_interval += 1
                    logger.debug("s", end="", flush=True)
                    continue
                elif error == "expired_token":
                    # The device code has expired
                    logger.error("Device code expired. Please try again.")
                    return None
                elif error == "access_denied":
                    # The user declined the authorization
                    logger.error("Authorization declined by user.")
                    return None
                else:
                    # Some other error
                    logger.error(f"Error: {error}")
                    return None
            else:
                # Unexpected response
                logger.error(f"Unexpected response: {token_response.status_code} - {token_response.text}")
                return None
        
        # If we get here, we timed out
        logger.error("Authentication timed out. Please try again.")
        return None
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        return None

def get_authenticated_client(force_login=False):
    """Get an authenticated client
    
    Args:
        force_login: Whether to force a new login
        
    Returns:
        MeshClient: An authenticated client
    """
    # Import here to avoid circular imports
    from .client import MeshClient
    
    # Check for existing token
    token_data = None if force_login else get_token()
    
    # Authenticate if needed
    if not token_data or not is_token_valid(token_data):
        # Try browser-based auth first
        token_data = authenticate()
        
        # Fall back to device flow
        if not token_data:
            token_data = authenticate_device_flow()
        
        # Still no token? Fail
        if not token_data:
            raise RuntimeError("Authentication failed. Please try again.")
    
    # Create client with token
    client = MeshClient()
    client.auth_token = token_data["access_token"]
    
    return client

def refresh_auth_token(auth0_domain=None, client_id=None, client_secret=None, refresh_token=None, audience=None, try_alternate=False):
    """
    Refresh an Auth0 token using the refresh token.
    
    Args:
        auth0_domain: Auth0 domain
        client_id: Auth0 client ID
        client_secret: Auth0 client secret
        refresh_token: Refresh token to use
        audience: Auth0 audience
        try_alternate: Whether to try alternate refresh methods if the first one fails
        
    Returns:
        dict: New token data or None if refresh failed
    """
    # Get Auth0 configuration if not provided
    auth0_config = get_auth0_config()
    
    auth0_domain = auth0_domain or auth0_config.get("domain") or AUTH0_DOMAIN
    client_id = client_id or auth0_config.get("client_id") or AUTH0_CLIENT_ID
    client_secret = client_secret or auth0_config.get("client_secret") or AUTH0_CLIENT_SECRET
    audience = audience or auth0_config.get("audience") or AUTH0_AUDIENCE
    
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
    
    # Try backend-driven refresh first (preferred)
    try:
        # Try to refresh using the backend
        response = requests.post(
            get_token_exchange_endpoint(),
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
    except Exception as e:
        logger.warning(f"Backend-driven token refresh failed: {str(e)}")
        
        # If we're not trying alternate methods, return None
        if not try_alternate:
            return None
    
    # If backend-driven refresh failed and we're allowed to try alternate methods,
    # try direct Auth0 refresh
    if try_alternate:
        try:
            # Try direct Auth0 refresh
            token_url = f"https://{auth0_domain}/oauth/token"
            token_data = {
                "grant_type": "refresh_token",
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token
            }
            
            response = requests.post(
                token_url,
                json=token_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                token_data = response.json()
                
                # Add expires_at for convenience
                if "expires_in" in token_data:
                    token_data["expires_at"] = int(time.time()) + token_data["expires_in"]
                
                # If the response doesn't include a refresh token, add the one we used
                if "refresh_token" not in token_data:
                    token_data["refresh_token"] = refresh_token
                
                # Store the new token
                store_token(token_data)
                
                logger.info("Successfully refreshed token using direct Auth0 refresh")
                return token_data
            else:
                logger.warning(f"Direct Auth0 token refresh failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.warning(f"Direct Auth0 token refresh failed: {str(e)}")
            return None
    
    return None 