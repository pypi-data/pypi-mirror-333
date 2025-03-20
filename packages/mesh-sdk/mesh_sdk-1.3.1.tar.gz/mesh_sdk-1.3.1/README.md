# Mesh SDK for Python

The Mesh SDK is a Python client library for the Mesh API. It provides a simple interface for authenticating with the API and making requests to the various endpoints.

## Installation

You can install the Mesh SDK from PyPI:

```bash
pip install mesh-sdk
```

Or directly from this repository:

```bash
pip install git+https://github.com/meshapi/mesh-sdk.git
```

## Features

- Easy authentication with OAuth 2.0 flows
- Automatic token refresh
- Both browser-based and headless device flow authentication
- Secure token storage using system keychain
- Comprehensive error handling
- Simple interface for chat completions with various AI models

## Usage

### Basic Usage

```python
from mesh_sdk import MeshClient

# Create a client (will automatically handle authentication if needed)
client = MeshClient()

# Send a chat message
response = client.chat("Hello, how are you today?", model="claude-3-7-sonnet")
print(response)
```

### Authentication

Authentication is handled automatically when needed. However, you can explicitly authenticate:

```python
from mesh_sdk import auth

# Trigger browser-based authentication
token_data = auth.authenticate()

# Or use headless/device flow authentication
token_data = auth.authenticate(headless=True)
```

You can also use the CLI tool for authentication:

```bash
# Authenticate using browser-based flow
mesh-auth

# Show help
mesh-auth --help
```

### Using the AutoRefreshMeshClient

The AutoRefreshMeshClient automatically refreshes expired tokens and manages token persistence:

```python
from mesh_sdk import AutoRefreshMeshClient

# Create client with auto-refresh enabled
client = AutoRefreshMeshClient()

# Use just like regular MeshClient
response = client.chat("Hello!", model="gpt-4o")
print(response)
```

## Development

To set up a development environment:

```bash
# Clone the repository
git clone https://github.com/meshapi/mesh-sdk.git
cd mesh-sdk/sdk/python/mesh_sdk_package

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
pip install -e .

# Run tests
python -m test_auth_module config
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.