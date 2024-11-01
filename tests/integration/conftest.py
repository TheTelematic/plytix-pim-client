from datetime import datetime
from typing import Callable

import httpx
import pytest

from plytix_pim_client import config


@pytest.fixture(scope="session", autouse=True)
def check_env_vars():
    assert config.PLYTIX_API_KEY, "PLYTIX_API_KEY environment variable is not set"
    assert config.PLYTIX_API_PASSWORD, "PLYTIX_API_PASSWORD environment variable is not set"
    config.USER_AGENT = f"[Integration Tests] {config.USER_AGENT}"


@pytest.fixture
def new_asset_data_from_url_factory() -> Callable[[], dict]:
    def factory() -> dict:
        with httpx.Client() as client:
            response = client.get("https://picsum.photos/200/300")
            return dict(
                url=response.headers["Location"],
                filename=f"test-{str(datetime.now().timestamp()).replace('.', '')}.jpg",
            )

    return factory
