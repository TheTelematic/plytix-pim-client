# plytix-pim-client
An HTTP client in Python for Plytix PIM API.

API documentation: https://apidocs.plytix.com

![Example](https://raw.githubusercontent.com/TheTelematic/plytix-pim-client/main/doc/images/example.png)

## Installation
```bash
pip install plytix-pim-client
```
Pypi: https://pypi.org/project/plytix-pim-client/

## Requirements
- Python 3.11+

## Features
- Synchronous and asynchronous clients
- Automatic token refresh
- Automatic rate limiting
- Automatic pagination
- Automatic error handling
- Automatic request retries
- API docs fully covered

## Usage

### Synchronous client
```python
from plytix_pim_client import PlytixPimClientSync

# Set the environment variables PLYTIX_API_KEY and PLYTIX_API_PASSWORD
client = PlytixPimClientSync()
```

### Asynchronous client
```python
from plytix_pim_client import PlytixPimClientAsync

# Set the environment variables PLYTIX_API_KEY and PLYTIX_API_PASSWORD
client = PlytixPimClientAsync()
```

All methods are available in both synchronous and asynchronous clients with the same I/O interface.
For the sake of simplicity, only the synchronous client is shown in the examples.

### Available resources
- `products`
- `families`

## Examples
### Create a product
```python
from plytix_pim_client import PlytixPimClientSync
client = PlytixPimClientSync()

client.products.create_product(sku="My First Product", label="My First Product")
```
