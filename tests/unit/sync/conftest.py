from typing import Generator

import pytest

from plytix_pim_client.client import PlytixSync


@pytest.fixture()
def plytix() -> Generator[PlytixSync, None, None]:
    _plytix = PlytixSync(response_cooldown_seconds=2.0)
    yield _plytix
    _plytix.close()
