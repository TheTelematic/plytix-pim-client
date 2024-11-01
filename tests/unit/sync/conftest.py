from typing import Callable
from unittest.mock import Mock

import httpx
import pytest

from plytix_pim_client.client import PlytixAsync
from plytix_pim_client.http.async_ import AsyncClient


@pytest.fixture
def mock_requests() -> Mock:
    return Mock(spec=httpx.AsyncClient)


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
