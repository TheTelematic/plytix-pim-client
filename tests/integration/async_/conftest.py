from typing import AsyncGenerator

import pytest

from plytix_pim_client.client import PlytixAsync


@pytest.fixture(scope="session")
async def plytix() -> AsyncGenerator[PlytixAsync, None]:
    _plytix = PlytixAsync()
    yield _plytix
    await _plytix.close()
