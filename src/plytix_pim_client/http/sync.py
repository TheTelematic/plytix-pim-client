import time
from http import HTTPMethod, HTTPStatus
from typing import List

import httpx

from plytix_pim_client import config
from plytix_pim_client.exceptions import RateLimitExceededError, TokenExpiredError
from plytix_pim_client.http.base import ClientBase
from plytix_pim_client.logger import logger


class SyncClient(ClientBase):
    def __init__(self, api_key: str | None = None, api_password: str | None = None, **kwargs):
        super().__init__(api_key, api_password, **kwargs)
        self.client = httpx.Client(
            base_url=self.base_url_pim,
            transport=httpx.HTTPTransport(retries=config.HTTP_RETRIES),
            timeout=config.HTTP_TIMEOUT,
        )

    def close(self):
        self.client.close()

    def make_request(
        self,
        method: HTTPMethod,
        path: str,
        waiting_time: float = 1.0,
        accepted_error_codes: List[HTTPStatus] | None = None,
        **kwargs,
    ) -> httpx.Response:
        kwargs["headers"] = self._get_headers()
        response = self.client.request(method, path, **kwargs)
        try:
            processed_response = self._process_response(response, accepted_error_codes=accepted_error_codes)
            if self._response_cooldown_seconds:
                logger.debug(f"Sleeping for {self._response_cooldown_seconds} seconds...")
                time.sleep(self._response_cooldown_seconds)
            return processed_response
        except TokenExpiredError:
            logger.debug("Token expired, refreshing token...")
            self._refresh_token()
            return self.make_request(method, path, accepted_error_codes=accepted_error_codes, **kwargs)
        except RateLimitExceededError:
            retry_after = float(response.headers.get("Retry-After", -1))
            if retry_after > 0:
                waiting_time = retry_after
            else:
                logger.warning("Rate limit exceeded, Retry-After header not found, making incremental waiting...")

            logger.warning(f"Rate limit exceeded, waiting {waiting_time} seconds before retrying...")
            time.sleep(waiting_time)
            waiting_time *= 2
            return self.make_request(
                method, path, waiting_time=waiting_time, accepted_error_codes=accepted_error_codes, **kwargs
            )

    def _refresh_token(self):
        response = self.client.post(
            f"{self.base_url_auth}/auth/api/get-token",
            json={"api_key": self.api_key, "api_password": self.api_password},
        )
        response.raise_for_status()
        self.auth_token = response.json()["data"][0]["access_token"]
