from plytix_pim_client.http.async_ import AsyncClient
from plytix_pim_client.http.sync import SyncClient
from plytix_pim_client.mixins import _ProductsAPISync, _ProductsAPIAsync, _FamiliesAPISync, _FamiliesAPIAsync


class PlytixPimClientSync:
    def __init__(self, api_key: str | None = None, api_password: str | None = None):
        self._client = SyncClient(api_key, api_password)

    def close(self):
        self._client.close()

    @property
    def products(self) -> _ProductsAPISync:
        return _ProductsAPISync(self._client)

    @property
    def families(self) -> _FamiliesAPISync:
        return _FamiliesAPISync(self._client)


class PlytixPimClientAsync:
    def __init__(self, api_key: str | None = None, api_password: str | None = None):
        self._client = AsyncClient(api_key, api_password)

    async def close(self):
        await self._client.close()

    @property
    def products(self) -> _ProductsAPIAsync:
        return _ProductsAPIAsync(self._client)

    @property
    def families(self) -> _FamiliesAPIAsync:
        return _FamiliesAPIAsync(self._client)
