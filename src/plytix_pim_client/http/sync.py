import threading
import time
from http import HTTPMethod, HTTPStatus
from typing import List

import httpx

from plytix_pim_client import config
from plytix_pim_client.constants import DEFAULT_WAIT_SECONDS_AFTER_AUTH_TOO_MANY_REQUESTS
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
        self._lock = threading.Lock()

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
        try:
            response = self.client.request(method, path, **kwargs)
        except httpx.TimeoutException:
            if not kwargs.get("fail_if_timeout", False):
                logger.warning(f"Timeout, retrying after {waiting_time} seconds...")
                time.sleep(waiting_time)
                return self.make_request(method, path, waiting_time, accepted_error_codes, fail_if_timeout=True)
            else:
                raise
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
        if self._lock.acquire(blocking=False):
            try:
                retry = True
                while retry:
                    response = self.client.post(
                        f"{self.base_url_auth}/auth/api/get-token",
                        json={"api_key": self.api_key, "api_password": self.api_password},
                    )
                    try:
                        response.raise_for_status()
                        retry = False
                    except httpx.HTTPStatusError as exc:
                        if exc.response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                            retry_after = float(
                                exc.response.headers.get(
                                    "Retry-After", DEFAULT_WAIT_SECONDS_AFTER_AUTH_TOO_MANY_REQUESTS
                                )
                            )
                            logger.error(
                                f"Auth get token is returning TooManyRequests error, "
                                f"retrying after {retry_after} seconds..."
                            )
                            time.sleep(retry_after)
                        elif exc.response.status_code in [HTTPStatus.BAD_GATEWAY, HTTPStatus.SERVICE_UNAVAILABLE]:
                            logger.error(
                                f"Auth get token is returning {exc.response.status_code} error, "
                                "retrying after 5 seconds..."
                            )
                            time.sleep(5)
                        else:
                            raise

                self.auth_token = response.json()["data"][0]["access_token"]
            finally:
                self._lock.release()
        else:
            while self._lock.locked():
                logger.warning("Another thread is refreshing the token, waiting...")
                time.sleep(1)
