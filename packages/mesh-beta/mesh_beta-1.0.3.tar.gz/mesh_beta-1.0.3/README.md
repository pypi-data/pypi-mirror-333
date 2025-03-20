# Mesh SDK for Python

A powerful Python SDK for interacting with the Mesh API, featuring key management, Zero-Knowledge Proofs, and AI chat capabilities.

## Quick Start

```bash
# Install the SDK
pip install mesh-beta

# When you first use the SDK, you'll be prompted to authenticate
# The SDK will display a URL and code for you to complete authentication
```

```python
import mesh

# First-time use will trigger authentication
# You'll see a URL and code to enter in your browser
response = mesh.chat("Hello, world!")
```

## Authentication

The first time you use the SDK, you'll need to authenticate. The SDK will automatically start the authentication process and display a URL and code for you to enter in your browser.

If automatic authentication fails, you can manually authenticate by running:

```bash
mesh-auth
```

For headless environments (servers without browsers):

```bash
mesh-auth --headless
```

## Installation

```bash
pip install mesh-beta
```

For development:

```bash
git clone https://github.com/yourusername/mesh.git
cd mesh/sdk/python
pip install -e .
```

## Features

- **Authentication**: Secure authentication with Auth0, including auto-refresh capabilities
- **Key Management**: Store and retrieve keys with optional Zero-Knowledge Proof verification
- **Chat Integration**: Easy-to-use interface for OpenAI and Anthropic models
- **Configurability**: Extensive configuration options via environment variables

## Quick Start

```python
from mesh import MeshClient

# Initialize the client
client = MeshClient()

# Chat with an AI model
response = client.chat("Hello, world!")
print(response['content'])

# Store a key (user_id is automatically extracted from your token)
client.store_key(key_name="api_key", key_value="secret_value")

# Get a key (user_id is automatically extracted from your token)
key_result = client.get_key(key_name="api_key")
```

## Authentication

The SDK supports several authentication methods:

1. **Direct token authentication** - Provide an `auth_token` when initializing the client
2. **Browser-based authentication** - Authentication via Auth0 will be triggered automatically when needed
3. **Environment variables** - Set `MESH_AUTH_TOKEN` in your environment

```python
# Direct token
client = MeshClient(auth_token="your_token")

# If no token is provided, browser-based auth will be triggered when needed
client = MeshClient()
response = client.chat("This will trigger auth if needed")
```

## Key Management

The SDK now automatically extracts your user ID from your authentication token, making key management simpler:

```python
# Store a key (user_id is extracted from your token)
client.store_key(key_name="openai_key", key_value="sk-abcdef123456")

# Get a key (user_id is extracted from your token)
key_result = client.get_key(key_name="openai_key")

# List all keys for the current user
keys = client.list_keys()
print(keys)  # ['openai_key', 'anthropic_key', 'api_key', ...]

# You can still provide a user_id manually if needed
client.store_key(user_id="custom-user-id", key_name="api_key", key_value="secret_value")
client.list_keys(user_id="custom-user-id")  # List keys for a specific user
```

## Configuration

The SDK offers extensive configuration options that can be set through environment variables or directly in code.

### Environment Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `AUTH0_DOMAIN` | Auth0 domain | (Configure in environment) |
| `AUTH0_CLIENT_ID` | Auth0 client ID | (Configure in environment) |
| `AUTH0_CLIENT_SECRET` | Auth0 client secret | (Secure value) |
| `AUTH0_AUDIENCE` | Auth0 audience | (Configure in environment) |
| `AUTH0_CALLBACK_PORT` | Port for Auth0 callback | 8000 |
| `MESH_API_URL` | Mesh API server URL | (Configure in environment) |
| `DEBUG` | Enable debug logging | false |
| `AUTO_REFRESH` | Enable automatic token refresh | true |
| `DEFAULT_OPENAI_MODEL` | Default OpenAI model | gpt-4 |
| `DEFAULT_ANTHROPIC_MODEL` | Default Anthropic model | claude-3-opus-20240229 |
| `DEFAULT_PROVIDER` | Default AI provider | openai |

### Configuration in Code

You can also configure the SDK directly in code:

```python
from mesh import MeshClient

# Override defaults in the constructor
client = MeshClient(
    server_url="https://custom-server.example.com",
    client_id="your-client-id",
    client_secret="your-client-secret",
    audience="your-audience",
    auth0_domain="your-domain.auth0.com",
    original_response=True  # Return raw API responses
)
```

### Auto-Refresh Client

For long-running applications, use the `AutoRefreshMeshClient` that can automatically refresh authentication tokens:

```python
from mesh.auto_refresh_client import AutoRefreshMeshClient

# Create an auto-refresh client
client = AutoRefreshMeshClient(
    auto_refresh=True,  # Enable auto-refresh (default if not specified)
    refresh_margin=300  # Refresh 5 minutes before expiry
)
```

## Advanced Usage

### Using Different Models

You can specify different AI models:

```python
# OpenAI models
response = client.chat("Tell me about quantum computing", model="gpt-4")

# Anthropic models
response = client.chat("Tell me about biology", 
                      model="claude-3-opus-20240229",
                      provider="anthropic")
```

### Zero-Knowledge Proofs

Store and verify keys with zero-knowledge proofs:

```python
# Store with ZKP
client.store_key_zkp("user123", "api_key", "secret_value")

# Verify with ZKP
result = client.verify_key("user123", "api_key", "secret_value")
```

## Error Handling

The SDK provides detailed error information:

```python
response = client.chat("Hello")
if not response.get("success", True):
    print(f"Error: {response.get('error')}")
    print(f"Details: {response.get('details')}")
    
    # For troubleshooting guidance
    if "troubleshooting" in response:
        print("Troubleshooting steps:")
        for step in response["troubleshooting"]:
            print(f"- {step}")
```

## Debugging

Enable debug mode for verbose logging:

```python
# Via environment variable
os.environ["DEBUG"] = "true"

# Or in code
client = MeshClient(debug=True)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Connection Issues
- Verify that the server URL is correct. By default, the SDK uses `https://mesh-abh5.onrender.com`.
- Check that the server is running and accessible from your network.
- If you're using a custom server, ensure it's properly configured and running.

### Endpoint Availability
- The SDK tries multiple endpoints to ensure compatibility with different server configurations.
- If you're getting "All endpoints failed" errors, check that the server has the required endpoints enabled.
- The SDK supports both new API endpoints (under `/api/v1/`) and legacy endpoints (under `/v1/mesh/`).

### Authentication Errors
- Ensure you have a valid authentication token. Run `mesh-auth` to authenticate manually.
- Check that your Auth0 credentials are correct if using browser-based authentication.
- Verify that your token hasn't expired. Tokens typically expire after a certain period.

### User Registration
- Chat functionality requires the user to be registered in the database.
- The SDK automatically attempts to register the user by calling the profile endpoint before the first chat request.
- If you're getting "User not found" errors, try calling the auth profile endpoint directly first.

### Message Format
- When using the chat functionality, ensure your messages are properly formatted.
- The SDK supports both "message" and "prompt" formats for compatibility with different server configurations.
- If you're getting format errors, check the server's expected message format.

### Debug Logging
- Enable debug logging by setting `debug=True` when initializing the client.
- This will provide detailed information about the requests and responses.
- Debug logs can help identify the root cause of issues.

## Advanced Configuration

```python
# Environment variables for configuration
# MESH_API_URL - Base server URL
# OPENAI_API_KEY - OpenAI API key
# ANTHROPIC_API_KEY - Anthropic API key
# DEFAULT_PROVIDER - Default AI provider
# DEFAULT_MODEL - Default model to use

# Set default model for a provider
client.set_default_model("openai", "gpt-4")
client.set_default_model("anthropic", "claude-3-7-sonnet-20250219")

# Reset to original defaults
client.reset_default_models()
```

## API Reference

For complete API documentation, please refer to the docstrings in the code.

## Chat Functionality

The SDK provides a simple interface to chat with AI models:

```python
# Chat with default model
response = client.chat("Hello, world!")

# Chat with specific model
response = client.chat("Hello, world!", model="gpt-4o", provider="openai")

# Enable thinking mode (Claude 3.7 Sonnet only)
response = client.chat("Solve this complex problem...", model="claude-3-7-sonnet-20250219", thinking=True)

# Get raw API response
response = client.chat("Hello, world!", original_response=True)
```

### Automatic User Registration

The SDK automatically ensures that the user is registered in the database before sending chat requests. This is necessary because the chat endpoints require the user to exist in the database. The registration process happens transparently when you make your first chat request:

```python
# The first chat request will automatically register the user if needed
response = client.chat("Hello, world!")
```

If the user registration fails, the SDK will return an error with troubleshooting steps:

```python
{
    "success": False,
    "error": "Failed to register user. Chat requires user registration.",
    "troubleshooting": [
        "Try calling the auth profile endpoint directly first",
        "Verify your authentication token is valid",
        "Check that the server URL is correct"
    ]
}
```

### Helper Methods

The SDK also provides helper methods for common chat scenarios:

```python
# Chat with GPT-4o
response = client.chat_with_gpt4o("Hello, world!")

# Chat with Claude
response = client.chat_with_claude("Hello, world!")

# Chat with the best model for a provider
response = client.chat_with_best_model("Hello, world!", provider="openai")

# Chat with the fastest model for a provider
response = client.chat_with_fastest_model("Hello, world!", provider="anthropic")

# Chat with the cheapest model for a provider
response = client.chat_with_cheapest_model("Hello, world!")
```

### Using Claude Models

The Mesh SDK supports Anthropic's Claude models and provides several ways to use them:

```python
from mesh import MeshClient

client = MeshClient()

# Method 1: Use the built-in helper method (recommended)
response = client.chat_with_claude("Write a haiku about programming")

# Specify Claude version
response = client.chat_with_claude("Write a haiku about programming", version="3.7")  # Use Claude 3.7
response = client.chat_with_claude("Write a haiku about programming", version="3")    # Use Claude 3 Opus

# Method 2: Specify the provider and model explicitly
response = client.chat(
    message="Write a haiku about programming",
    model="claude-3-7-sonnet-20250219",
    provider="anthropic"
)

# Method 3: Use a model alias (which maps to a specific version)
response = client.chat(
    message="Write a haiku about programming",
    model="claude-37"  # Aliased to claude-3-7-sonnet-20250219
)
```

#### Claude Model Aliases

The SDK provides several aliases for Claude models to make them easier to use:

| Alias           | Maps to                     | Description              |
|-----------------|----------------------------|--------------------------|
| `claude`        | claude-3-5-sonnet-20241022 | Latest stable Claude     |
| `claude-37`     | claude-3-7-sonnet-20250219 | Claude 3.7 Sonnet        |
| `claude-35`     | claude-3-5-sonnet-20241022 | Claude 3.5 Sonnet        |
| `claude-35-haiku` | claude-3-5-haiku-20241022 | Claude 3.5 Haiku        |
| `claude-3`      | claude-3-opus-20240229    | Claude 3 Opus            |
| `claude-opus`   | claude-3-opus-20240229    | Claude 3 Opus            |
| `claude-sonnet` | claude-3-sonnet-20240229  | Claude 3 Sonnet          |
| `claude-haiku`  | claude-3-haiku-20240307   | Claude 3 Haiku           |

> **Note:** When using the `claude` alias directly, it's mapped to a specific version of Claude (currently Claude 3.5 Sonnet) for stability. This may not be the absolute latest Claude model. For the most reliable way to use specific Claude versions:
> - Use `chat_with_claude(message, version="3.7")` to explicitly select the version
> - Or specify the full model ID with `model="claude-3-7-sonnet-20250219"` 

## Simplified API

The SDK also provides a simplified API that can be used directly without creating a client instance:

```python
import mesh

# Chat with an AI model
response = mesh.chat("Hello, world!")

# Store a key
mesh.store_key(key_name="api_key", key_value="secret_value")

# Get a key
key_value = mesh.get_key(key_name="api_key")

# List all keys for the current user
keys = mesh.list_keys()
print(keys)  # ['api_key', 'openai_key', 'anthropic_key', ...]

# List keys for a specific user
keys = mesh.list_keys(user_id="custom-user-id")
```

This simplified API is perfect for quick scripts and applications where you don't need the full flexibility of the client instance.

## Authentication Troubleshooting

If you encounter authentication issues when using the SDK, here are some common problems and solutions:

### Port Already in Use

The SDK uses a local server on port 8000 (by default) to handle the OAuth callback. If this port is already in use, the SDK will now automatically try ports 8000-8009 until it finds an available one.

If all ports are in use, you can:
- Close applications that might be using these ports
- Specify a different port: `mesh-auth --port 9000`
- Use the headless authentication method: `mesh-auth --headless`

### Browser Not Opening

If the SDK fails to open a browser automatically, it will now display a URL that you can manually copy and paste into your browser.

### Authentication Server Errors

If you see "Failed to start authentication server" errors:
- Check if your firewall is blocking the local server
- Try the headless authentication method: `mesh-auth --headless`
- Ensure you have network connectivity to the Auth0 domain

### Headless Environments

For servers or environments without a browser:
```bash
# Use the device code flow
mesh-auth --headless
```
This will display a URL and a code that you can use on another device to authenticate.

### Automatic Authentication

The SDK now attempts to authenticate automatically when you first use it:
1. First using device code flow (which doesn't require a local server)
2. Then falling back to browser-based authentication if needed
3. Trying multiple ports if the default port is in use

If automatic authentication fails, you'll need to run `mesh-auth` manually. 

## Auth0 Configuration

For the SDK to work properly, you need to configure your Auth0 application correctly:

### Device Code Flow Configuration

To enable the device code flow (used for headless authentication):

1. Log in to your Auth0 dashboard
2. Go to "Applications" > Select your application
3. Go to the "Settings" tab
4. Under "Advanced Settings" > "Grant Types"
5. Make sure "Device Code" is checked
6. Under "Advanced Settings" > "Device Settings"
7. Enable "Device Flow with Polling"

### API Configuration

1. Go to "APIs" > Select your API
2. Under "Settings"
3. Enable "Allow Offline Access" to get refresh tokens
4. Make sure the appropriate grant types are enabled

### Callback URLs

For browser-based authentication, add the following to "Allowed Callback URLs":
```
http://localhost:45678/callback
```

The SDK now uses port 45678 by default, which is less likely to conflict with other applications. 