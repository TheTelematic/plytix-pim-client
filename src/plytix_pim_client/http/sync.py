import time
from http import HTTPMethod

import httpx

from plytix_pim_client.constants import DEFAULT_HTTP_RETRIES, DEFAULT_HTTP_TIMEOUT
from plytix_pim_client.exceptions import TokenExpiredError, RateLimitExceededError
from plytix_pim_client.http.base import ClientBase
from plytix_pim_client.logger import logger


class SyncClient(ClientBase):
    def __init__(self, api_key: str | None = None, api_password: str | None = None, base_url: str | None = None):
        super().__init__(api_key, api_password, base_url)
        self.client = httpx.Client(
            base_url=self.base_url_pim,
            transport=httpx.HTTPTransport(retries=DEFAULT_HTTP_RETRIES),
            timeout=DEFAULT_HTTP_TIMEOUT,
        )

    def close(self):
        self.client.close()

    def make_request(self, method: HTTPMethod, path: str, waiting_time: float = 1.0, **kwargs) -> httpx.Response:
        kwargs["headers"] = self._get_auth_headers()
        response = self.client.request(method, path, **kwargs)
        try:
            return self._process_response(response)
        except TokenExpiredError:
            logger.debug("Token expired, refreshing token...")
            self._refresh_token()
            return self.make_request(method, path, **kwargs)
        except RateLimitExceededError:
            logger.warning(f"Rate limit exceeded, waiting {waiting_time} seconds before retrying...")
            time.sleep(waiting_time)
            waiting_time *= 2
            return self.make_request(method, path, waiting_time=waiting_time, **kwargs)

    def _refresh_token(self):
        response = self.client.post(
            f"{self.base_url_auth}/auth/api/get-token",
            json={"api_key": self.api_key, "api_password": self.api_password},
        )
        response.raise_for_status()
        self.auth_token = response.json()["data"][0]["access_token"]
