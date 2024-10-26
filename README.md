# plytix-pim-client
An HTTP client in Python for Plytix PIM API.

![PyPI](https://img.shields.io/pypi/v/plytix-pim-client?label=pypi%20package)
![PyPI - Downloads](https://img.shields.io/pypi/dm/plytix-pim-client)
![GitHub Action Publish to PyPI](https://github.com/TheTelematic/plytix-pim-client/actions/workflows/publish-to-pypi.yml/badge.svg)

API documentation: https://apidocs.plytix.com

![Example](https://raw.githubusercontent.com/TheTelematic/plytix-pim-client/main/doc/images/example.png)

## Installation
```bash
pip install plytix-pim-client
```
PyPI: https://pypi.org/project/plytix-pim-client/

## Requirements
- Python 3.11+

## Features
- Synchronous and asynchronous clients
- Automatic token refresh
- Automatic rate limiting
- Automatic pagination
- Automatic error handling
- Automatic request retries
- API docs fully covered*
- Configurable Response Cooldown

## Usage

### Synchronous client

```python
from plytix_pim_client import PlytixSync

# Set the environment variables PLYTIX_API_KEY and PLYTIX_API_PASSWORD
plytix = PlytixSync()
```

### Asynchronous client

```python
from plytix_pim_client import PlytixAsync

# Set the environment variables PLYTIX_API_KEY and PLYTIX_API_PASSWORD
plytix = PlytixAsync()
```

All methods are available in both synchronous and asynchronous clients with the same I/O interface.
For the sake of simplicity, only the synchronous client is shown in the examples.

### Available resources
Any of the following resources can be accessed through the client:
- `products`
  - `assets`
  - `attributes`
    - `groups`
  - `categories`
  - `families`
    - `attributes`
  - `relationships`
  - `variants`
- `assets`
  - `categories`

Each resource has specific methods to interact with the API. 
If you use an IDE with code completion, you can see all available methods.
If you find a method that is not available or confusing, please open an issue.
Also, you may have a look to the integration tests for more examples.

## Examples
### Create a product

```python
from plytix_pim_client import PlytixSync

plytix = PlytixSync()

plytix.products.create_product(sku="My First Product", label="My First Product")
```

### Create a product family

```python
from plytix_pim_client import PlytixSync

plytix = PlytixSync()

plytix.products.families.create_family(name="My First Family")
```


## * Known issues
Check out the [open Issues with "bug" label](https://github.com/TheTelematic/plytix-pim-client/issues?q=is%3Aopen+is%3Aissue+label%3Abug).
