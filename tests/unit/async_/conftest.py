from typing import AsyncGenerator

import pytest

from plytix_pim_client.client import PlytixAsync


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[PlytixAsync, None]:
    _client = PlytixAsync()
    yield _client
    await _client.close()
