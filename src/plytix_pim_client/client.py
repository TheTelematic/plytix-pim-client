from plytix_pim_client.http.async_ import AsyncClient
from plytix_pim_client.http.sync import SyncClient
from plytix_pim_client.mixins import (
    _AssetsAPIAsync,
    _AssetsAPISync,
    _ProductsAPIAsync,
    _ProductsAPISync,
    _FiltersAPISync,
    _FiltersAPIAsync,
)


class PlytixSync:
    def __init__(self, api_key: str | None = None, api_password: str | None = None, **kwargs):
        self._client = SyncClient(api_key, api_password, **kwargs)

    def close(self):
        self._client.close()

    @property
    def assets(self) -> _AssetsAPISync:
        return _AssetsAPISync(self._client)

    @property
    def filters(self) -> _FiltersAPISync:
        return _FiltersAPISync(self._client)

    @property
    def products(self) -> _ProductsAPISync:
        return _ProductsAPISync(self._client)


class PlytixAsync:
    def __init__(self, api_key: str | None = None, api_password: str | None = None, **kwargs):
        self._client = AsyncClient(api_key, api_password, **kwargs)

    async def close(self):
        await self._client.close()

    @property
    def assets(self) -> _AssetsAPIAsync:
        return _AssetsAPIAsync(self._client)

    @property
    def filters(self) -> _FiltersAPIAsync:
        return _FiltersAPIAsync(self._client)

    @property
    def products(self) -> _ProductsAPIAsync:
        return _ProductsAPIAsync(self._client)
