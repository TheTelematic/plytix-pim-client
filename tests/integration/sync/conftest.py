from typing import Generator

import pytest

from plytix_pim_client.client import PlytixSync


@pytest.fixture(scope="session")
def plytix() -> Generator[PlytixSync, None, None]:
    _plytix = PlytixSync()
    yield _plytix
    _plytix.close()
