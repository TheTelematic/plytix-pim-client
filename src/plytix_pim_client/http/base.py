from http import HTTPStatus
from typing import List

import httpx

from plytix_pim_client import config
from plytix_pim_client.exceptions import (
    RateLimitExceededError,
    TokenExpiredError,
    UnprocessableEntityError,
    BadRequestError,
    ConflictError,
)
from plytix_pim_client.logger import logger


class ClientBase:

    def __init__(
        self,
        api_key: str | None = None,
        api_password: str | None = None,
        response_cooldown_seconds: float | None = None,
    ):
        self.api_key = api_key or config.PLYTIX_API_KEY
        self.api_password = api_password or config.PLYTIX_API_PASSWORD
        self.base_url_pim = config.PLYTIX_PIM_BASE_URL
        self.base_url_auth = config.PLYTIX_AUTH_BASE_URL
        self.auth_token: str | None = None
        self._response_cooldown_seconds = response_cooldown_seconds

        if not self.api_key or not self.api_password:
            raise ValueError(
                "API key and password are required, please pass to the client or "
                "set the env vars PLYTIX_API_KEY and PLYTIX_API_PASSWORD"
            )

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.auth_token}",
            "User-Agent": config.USER_AGENT,
        }

    @staticmethod
    def _process_response(
        response: httpx.Response, accepted_error_codes: List[HTTPStatus] | None = None
    ) -> httpx.Response:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            if accepted_error_codes and exc.response.status_code in accepted_error_codes:
                return exc.response

            if exc.response.status_code == HTTPStatus.UNAUTHORIZED:
                raise TokenExpiredError("Token expired")
            elif exc.response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                raise RateLimitExceededError("Rate limit exceeded")
            elif exc.response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
                message = (
                    f"Error with {exc.request.method} {exc.request.url} - "
                    f"Request Payload: {exc.request.content!r} Response: {exc.response.json()}"
                )
                logger.error(message)
                raise UnprocessableEntityError(message)
            elif exc.response.status_code == HTTPStatus.BAD_REQUEST:
                message = f"Error with {exc.request.method} {exc.request.url} - {exc.response.json()}"
                logger.error(message)
                raise BadRequestError(message)
            elif exc.response.status_code == HTTPStatus.CONFLICT:
                message = f"Error with {exc.request.method} {exc.request.url} - {exc.response.json()}"
                logger.error(message)
                raise ConflictError(message)
            else:
                raise exc

        return response
