from concurrent.futures import Future
from typing import Callable
from unittest.mock import Mock, patch

import httpx
import pytest

from plytix_pim_client.client import PlytixSync
from plytix_pim_client.http.sync import SyncClient


@pytest.fixture
def mock_requests() -> Mock:
    return Mock(spec=httpx.Client)


@pytest.fixture()
def plytix_factory(mock_requests, api_token) -> Callable[[list[httpx.Response]], PlytixSync]:
    def plytix(expected_responses: list[httpx.Response]) -> PlytixSync:
        mock_requests.request.side_effect = expected_responses

        mock_client = SyncClient()
        mock_client.client = mock_requests
        mock_client.auth_token = api_token

        _plytix = PlytixSync()
        _plytix._client = mock_client
        return _plytix

    return plytix


@pytest.fixture(scope="session", autouse=True)
def hook_threading_thread_pool_executor_submit():
    """Run sequentially all tasks submitted in the ThreadPoolExecutor."""

    def _sequential_submit(self, func, *args, **kwargs):
        future = Future()
        future.set_result(func(*args, **kwargs))
        return future

    with patch("concurrent.futures.thread.ThreadPoolExecutor.submit", new=_sequential_submit):
        yield
