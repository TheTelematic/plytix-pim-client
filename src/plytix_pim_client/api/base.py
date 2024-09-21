from plytix_pim_client.http.async_ import AsyncClient
from plytix_pim_client.http.sync import SyncClient


class BaseAPISyncMixin:
    def __init__(self, client: SyncClient):
        self._client = client


class BaseAPIAsyncMixin:
    def __init__(self, client: AsyncClient):
        self._client = client
