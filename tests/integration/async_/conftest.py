import pytest

from plytix_pim_client.client import PlytixPimClientAsync


@pytest.fixture(scope="session")
async def client() -> PlytixPimClientAsync:
    _client = PlytixPimClientAsync()
    yield _client
    await _client.close()
