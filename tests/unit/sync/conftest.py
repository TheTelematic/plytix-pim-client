import pytest

from plytix_pim_client.client import PlytixPimClientSync


@pytest.fixture(scope="session")
def client() -> PlytixPimClientSync:
    _client = PlytixPimClientSync()
    yield _client
    _client.close()
