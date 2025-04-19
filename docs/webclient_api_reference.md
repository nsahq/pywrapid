# Web Client API Reference

This document provides detailed API reference for the various web client implementations in the consolidated pywrapid package.

## Common Interface

All web client implementations follow the same interface defined in `pywrapid.interfaces.webclient.WebClientInterface`, which provides consistency across different HTTP libraries.

```python
class WebClientInterface(Protocol):
    """Interface for web client implementations.
    
    This interface defines the common methods that all web client
    implementations must provide, ensuring consistency across different
    backend libraries (requests, httpx, aiohttp).
    """
    
    def get(self, url: str, **kwargs) -> Any:
        """Send GET request to the specified URL."""
        ...
        
    def post(self, url: str, **kwargs) -> Any:
        """Send POST request to the specified URL."""
        ...
        
    def put(self, url: str, **kwargs) -> Any:
        """Send PUT request to the specified URL."""
        ...
        
    def delete(self, url: str, **kwargs) -> Any:
        """Send DELETE request to the specified URL."""
        ...
        
    def request(self, method: str, url: str, **kwargs) -> Any:
        """Send request with the specified method to the URL."""
        ...
```

## Authorization Types

The web client implementations support various authorization methods through the `AuthorizationType` enum:

```python
from pywrapid.webclient.enums import AuthorizationType

# Available authorization types
AuthorizationType.NONE       # No authentication
AuthorizationType.BASIC      # Basic authentication (username:password)
AuthorizationType.TOKEN      # Token authentication (Bearer token)
AuthorizationType.API_KEY    # API key authentication
AuthorizationType.JWT        # JWT token authentication
AuthorizationType.OAUTH2     # OAuth2 authentication
AuthorizationType.CUSTOM     # Custom authentication mechanism
```

## Requests Implementation (`RequestsWebClient`)

The requests implementation uses the popular [requests](https://requests.readthedocs.io/) library.

### RequestsWebClient

```python
from pywrapid.webclient.requests_client import RequestsWebClient
from pywrapid.webclient.enums import AuthorizationType

# Basic client with default parameters
client = RequestsWebClient(base_url="https://api.example.com")

# Client with authentication and custom settings
client = RequestsWebClient(
    base_url="https://api.example.com",
    timeout=30,                              # Request timeout in seconds
    auth_type=AuthorizationType.TOKEN,       # Authorization type
    credentials="your-token",                # Authorization credentials
    retries=3,                               # Number of automatic retries for failed requests
    verify=True                              # Verify SSL certificates
)

# Making requests
response = client.get("/users")              # GET request
response = client.post("/users", json={})    # POST request with JSON body
response = client.put("/users/1", json={})   # PUT request with JSON body
response = client.delete("/users/1")         # DELETE request

# Advanced usage
response = client.request(
    method="GET",
    url="/users",
    params={"page": 1, "limit": 10},         # Query parameters
    headers={"X-Custom-Header": "value"},    # Request-specific headers
    timeout=60                               # Override default timeout
)
```

## HTTPX Implementation (`HTTPXWebClient`)

The HTTPX implementation uses the modern [httpx](https://www.python-httpx.org/) library.

### HTTPXWebClient

```python
from pywrapid.webclient.httpx_client import HTTPXWebClient
from pywrapid.webclient.enums import AuthorizationType

# Basic client with default parameters
client = HTTPXWebClient(base_url="https://api.example.com")

# Client with authentication and custom settings
client = HTTPXWebClient(
    base_url="https://api.example.com",
    timeout=30,                              # Request timeout in seconds
    auth_type=AuthorizationType.TOKEN,       # Authorization type
    credentials="your-token",                # Authorization credentials
    follow_redirects=True,                   # Follow redirects automatically
    verify=True                              # Verify SSL certificates
)

# Making requests (same API as RequestsWebClient)
response = client.get("/users")
response = client.post("/users", json={})
response = client.put("/users/1", json={})
response = client.delete("/users/1")

# HTTP/2 support (automatic when supported by the server)
response = client.get("/users")
```

## Async Implementation (`AsyncWebClient`)

The async implementation uses the [aiohttp](https://docs.aiohttp.org/) library for asynchronous requests.

### AsyncWebClient

```python
import asyncio
from pywrapid.webclient.aiohttp_client import AsyncWebClient
from pywrapid.webclient.enums import AuthorizationType

async def main():
    # Use async context manager to ensure resources are properly cleaned up
    async with AsyncWebClient(
        base_url="https://api.example.com",
        timeout=30,                              # Request timeout in seconds
        auth_type=AuthorizationType.TOKEN,       # Authorization type
        credentials="your-token",                # Authorization credentials
    ) as client:
        # Making async requests
        response = await client.get("/users")
        response = await client.post("/users", json={})
        response = await client.put("/users/1", json={})
        response = await client.delete("/users/1")
        
        # Get response data
        data = await response.json()
        
        # Parallel requests
        tasks = [
            client.get("/users/1"),
            client.get("/users/2"),
            client.get("/users/3"),
        ]
        responses = await asyncio.gather(*tasks)
        
# Run the async code
asyncio.run(main())
```

## Common Parameters for All Implementations

All web client implementations support these common parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `base_url` | `str` | Base URL for the API. URLs passed to methods will be joined with this base URL |
| `timeout` | `int/float` | Request timeout in seconds (default: 30) |
| `auth_type` | `AuthorizationType` | Type of authentication to use |
| `credentials` | `str/tuple/dict` | Credentials for authentication |
| `headers` | `Dict[str, str]` | Default headers to include in every request |
| `verify` | `bool` | Whether to verify SSL certificates (default: True) |

## Using Smart Backend Detection

The pywrapid package includes smart backend detection that selects the best available implementation:

```python
from pywrapid.webclient import WebClient

# This will automatically use one of the available implementations
# with the following priority: requests > httpx > aiohttp
client = WebClient(base_url="https://api.example.com")
```

## Best Practices

1. **Use context managers with AsyncWebClient**: Always use the async context manager (`async with`) when working with AsyncWebClient to ensure proper resource cleanup.

2. **Set reasonable timeouts**: Always set a reasonable timeout to prevent your application from hanging indefinitely.

3. **Use exception handling**: Implement proper exception handling to gracefully handle API errors.

4. **Set meaningful user agents**: Set a descriptive user agent in your headers to identify your application.

5. **Consider rate limiting**: For APIs with rate limits, implement backoff strategies.
