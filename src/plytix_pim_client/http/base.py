from http import HTTPMethod, HTTPStatus

import httpx

from plytix_pim_client import config
from plytix_pim_client.exceptions import TokenExpiredError, RateLimitExceededError, UnprocessableEntityError
from plytix_pim_client.logger import logger


class ClientBase:
    method = HTTPMethod

    def __init__(self, api_key: str | None = None, api_password: str | None = None, base_url: str | None = None):
        self.api_key = api_key or config.PLYTIX_API_KEY
        self.api_password = api_password or config.PLYTIX_API_PASSWORD
        self.base_url_pim = base_url or config.PLYTIX_PIM_BASE_URL
        self.base_url_auth = config.PLYTIX_AUTH_BASE_URL
        self.auth_token: str | None = None

    def _get_auth_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.auth_token}",
        }

    @staticmethod
    def _process_response(response: httpx.Response) -> httpx.Response:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == HTTPStatus.UNAUTHORIZED:
                raise TokenExpiredError("Token expired")
            elif exc.response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                raise RateLimitExceededError("Rate limit exceeded")
            elif exc.response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
                message = f"Error with {exc.request.method} {exc.request.url} - {exc.response.json()}"
                logger.error(message)
                raise UnprocessableEntityError(message)
            else:
                raise exc

        return response
