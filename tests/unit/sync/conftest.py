from typing import Generator

import pytest

from plytix_pim_client.client import PlytixSync


@pytest.fixture(scope="session")
def client() -> Generator[PlytixSync, None, None]:
    _client = PlytixSync()
    yield _client
    _client.close()
