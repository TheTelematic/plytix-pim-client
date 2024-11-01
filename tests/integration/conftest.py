import pytest

from plytix_pim_client import config


@pytest.fixture(scope="session", autouse=True)
def check_env_vars():
    assert config.PLYTIX_API_KEY, "PLYTIX_API_KEY environment variable is not set"
    assert config.PLYTIX_API_PASSWORD, "PLYTIX_API_PASSWORD environment variable is not set"
    config.USER_AGENT = f"[Integration Tests] {config.USER_AGENT}"
