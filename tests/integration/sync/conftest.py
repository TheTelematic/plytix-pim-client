from typing import Generator

import pytest

from plytix_pim_client.client import PlytixPimClientSync


@pytest.fixture(scope="session")
def client() -> Generator[PlytixPimClientSync, None, None]:
    _client = PlytixPimClientSync()
    yield _client
    _client.close()
