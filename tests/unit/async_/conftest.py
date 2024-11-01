from typing import Callable
from unittest.mock import AsyncMock, patch

import httpx
import pytest

from plytix_pim_client.client import PlytixAsync
from plytix_pim_client.http.async_ import AsyncClient


@pytest.fixture
def mock_requests() -> AsyncMock:
    return AsyncMock(spec=httpx.AsyncClient)


@pytest.fixture()
def plytix_factory(mock_requests, api_token) -> Callable[[list[httpx.Response]], PlytixAsync]:
    def plytix(expected_responses: list[httpx.Response]) -> PlytixAsync:
        mock_requests.request.side_effect = expected_responses

        mock_client = AsyncClient()
        mock_client.client = mock_requests
        mock_client.auth_token = api_token

        _plytix = PlytixAsync()
        _plytix._client = mock_client
        return _plytix

    return plytix


@pytest.fixture(scope="function", autouse=True)
async def hook_asyncio_gather():
    """Run sequentially all tasks scheduled with asyncio.gather."""

    async def _sequential_gather(*tasks) -> list:
        results = []
        for task in tasks:
            results.append(await task)

        return results

    with patch("asyncio.gather", new=_sequential_gather):
        yield
