from http import HTTPStatus, HTTPMethod
from unittest.mock import Mock

import httpx
import pytest


@pytest.fixture
def mock_response() -> httpx.Response:
    return httpx.Response(status_code=HTTPStatus.OK, request=Mock())


async def test_happy_path(mock_requests, mock_http_client, mock_response):
    mock_requests.request.side_effect = [mock_response]

    response = await mock_http_client.make_request(HTTPMethod.GET, "/foo")

    assert response.status_code == HTTPStatus.OK
    assert response.content == b""


async def test_response_cooldown_seconds_is_set(mock_requests, mock_http_client, mock_response):
    mock_requests.request.side_effect = [mock_response]
    mock_http_client._response_cooldown_seconds = 1

    response = await mock_http_client.make_request(HTTPMethod.GET, "/foo")

    assert response.status_code == HTTPStatus.OK
    assert response.content == b""


async def test_token_expired(mock_requests, mock_http_client, mock_response):
    mock_requests.request.side_effect = [
        mock_response,
    ]
    mock_requests.post.side_effect = [
        httpx.Response(status_code=HTTPStatus.UNAUTHORIZED, request=Mock()),
        httpx.Response(status_code=HTTPStatus.OK, request=Mock(), json={"data": [{"access_token": "foo"}]}),
    ]

    response = await mock_http_client.make_request(HTTPMethod.GET, "/foo")

    assert response.status_code == HTTPStatus.OK
    assert response.content == b""
