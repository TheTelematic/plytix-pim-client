from plytix_pim_client.http.async_ import AsyncClient
from plytix_pim_client.http.sync import SyncClient
from plytix_pim_client.mixins import _ProductsAPISync, _ProductsAPIAsync, _AssetsAPISync, _AssetsAPIAsync


class PlytixSync:
    def __init__(self, api_key: str | None = None, api_password: str | None = None):
        self._client = SyncClient(api_key, api_password)

    def close(self):
        self._client.close()

    @property
    def assets(self) -> _AssetsAPISync:
        return _AssetsAPISync(self._client)

    @property
    def products(self) -> _ProductsAPISync:
        return _ProductsAPISync(self._client)


class PlytixAsync:
    def __init__(self, api_key: str | None = None, api_password: str | None = None):
        self._client = AsyncClient(api_key, api_password)

    async def close(self):
        await self._client.close()

    @property
    def assets(self) -> _AssetsAPIAsync:
        return _AssetsAPIAsync(self._client)

    @property
    def products(self) -> _ProductsAPIAsync:
        return _ProductsAPIAsync(self._client)
