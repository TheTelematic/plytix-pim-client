from typing import Callable
from unittest.mock import AsyncMock

import httpx
import pytest

from plytix_pim_client.client import PlytixAsync
from plytix_pim_client.http.async_ import AsyncClient


@pytest.fixture()
def plytix_factory() -> Callable[[list[httpx.Response]], tuple[PlytixAsync, AsyncMock]]:
    def plytix(expected_responses: list[httpx.Response]) -> tuple[PlytixAsync, AsyncMock]:
        mock_httpx_client = AsyncMock(spec=httpx.AsyncClient)
        mock_httpx_client.request.side_effect = expected_responses

        mock_client = AsyncMock(spec=AsyncClient)
        mock_client.client = mock_httpx_client

        _plytix = AsyncMock(spec=PlytixAsync)
        _plytix._client = mock_client
        return _plytix, mock_httpx_client.request

    return plytix
