from http import HTTPStatus, HTTPMethod
from typing import Callable, Optional, TypedDict, NotRequired
from unittest.mock import AsyncMock, Mock, call

import httpx
import pytest

from plytix_pim_client import config
from plytix_pim_client.client import PlytixAsync
from plytix_pim_client.http.async_ import AsyncClient


class ExpectedRequest(TypedDict):
    method: HTTPMethod
    path: str
    json: NotRequired[dict]
    files: NotRequired[dict]


@pytest.fixture
def mock_requests() -> AsyncMock:
    return AsyncMock(spec=httpx.AsyncClient)


@pytest.fixture()
def plytix_factory(mock_requests) -> Callable[[list[httpx.Response]], PlytixAsync]:
    def plytix(expected_responses: list[httpx.Response]) -> PlytixAsync:
        mock_requests.request.side_effect = expected_responses

        mock_client = AsyncClient()
        mock_client.client = mock_requests

        _plytix = PlytixAsync()
        _plytix._client = mock_client
        return _plytix

    return plytix


@pytest.fixture
def response_factory() -> Callable[[HTTPStatus, Optional[dict]], httpx.Response]:
    def factory(status_code: HTTPStatus, json: dict | list[dict] | None = None) -> httpx.Response:
        if json:
            json = {"data": [json]} if isinstance(json, dict) else {"data": json}

        return httpx.Response(request=Mock(), status_code=status_code, json=json)

    return factory


@pytest.fixture
def assert_requests_factory(mock_requests) -> Callable[[list[ExpectedRequest]], bool]:
    def factory(expected_requests: list[ExpectedRequest]) -> bool:
        assert mock_requests.request.call_args_list == [
            call(
                request["method"],
                request["path"],
                **{k: v for k, v in request.items() if k not in ["method", "path"]},
                headers={
                    "Authorization": "Bearer None",
                    "User-Agent": config.USER_AGENT,
                }
            )
            for request in expected_requests
        ]

        return True

    return factory
