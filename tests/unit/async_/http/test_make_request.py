from datetime import datetime
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
        httpx.Response(status_code=HTTPStatus.UNAUTHORIZED, request=Mock()),
        mock_response,
    ]
    mock_requests.post.side_effect = [
        httpx.Response(status_code=HTTPStatus.OK, request=Mock(), json={"data": [{"access_token": "foo"}]}),
    ]

    response = await mock_http_client.make_request(HTTPMethod.GET, "/foo")

    assert response.status_code == HTTPStatus.OK
    assert response.content == b""


async def test_token_expired_and_auth_too_many_requests(mock_requests, mock_http_client, mock_response):
    mock_requests.request.side_effect = [
        httpx.Response(status_code=HTTPStatus.UNAUTHORIZED, request=Mock()),
        mock_response,
    ]
    mock_requests.post.side_effect = [
        httpx.Response(status_code=HTTPStatus.TOO_MANY_REQUESTS, request=Mock(), headers={"Retry-After": "1"}),
        httpx.Response(status_code=HTTPStatus.OK, request=Mock(), json={"data": [{"access_token": "foo"}]}),
    ]

    response = await mock_http_client.make_request(HTTPMethod.GET, "/foo")

    assert response.status_code == HTTPStatus.OK
    assert response.content == b""


async def test_token_expired_previously_refreshed(mock_requests, mock_http_client, mock_response):
    mock_requests.request.side_effect = [
        httpx.Response(status_code=HTTPStatus.UNAUTHORIZED, request=Mock()),
        mock_response,
    ]
    mock_requests.post.side_effect = [
        httpx.Response(status_code=HTTPStatus.OK, request=Mock(), json={"data": [{"access_token": "foo"}]}),
    ]
    mock_http_client._token_refreshed_at = datetime.now().timestamp()

    response = await mock_http_client.make_request(HTTPMethod.GET, "/foo")

    assert response.status_code == HTTPStatus.OK
    assert response.content == b""


@pytest.mark.parametrize("headers", [None, {"Retry-After": "1"}])
async def test_rate_limit_exceeded(mock_requests, mock_http_client, mock_response, headers):
    mock_requests.request.side_effect = [
        httpx.Response(status_code=HTTPStatus.TOO_MANY_REQUESTS, request=Mock(), headers=headers),
        mock_response,
    ]

    response = await mock_http_client.make_request(HTTPMethod.GET, "/foo")

    assert response.status_code == HTTPStatus.OK
    assert response.content == b""
