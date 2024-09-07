from plytix_pim_client.api.products.create import ProductCreateAPISyncMixin, ProductCreateAPIAsyncMixin
from plytix_pim_client.api.products.search import ProductsSearchAPISyncMixin, ProductsSearchAPIAsyncMixin
from plytix_pim_client.http.async_ import AsyncClient
from plytix_pim_client.http.sync import SyncClient


class _ProductsAPISync(ProductCreateAPISyncMixin, ProductsSearchAPISyncMixin): ...


class _ProductsAPIAsync(ProductCreateAPIAsyncMixin, ProductsSearchAPIAsyncMixin): ...


class PlytixPimClientSync:
    def __init__(self, api_key: str | None = None, api_password: str | None = None, base_url: str | None = None):
        self._client = SyncClient(api_key, api_password, base_url)

    def close(self):
        self._client.close()

    @property
    def products(self) -> _ProductsAPISync:
        return _ProductsAPISync(self._client)


class PlytixPimClientAsync:
    def __init__(self, api_key: str | None = None, api_password: str | None = None, base_url: str | None = None):
        self._client = AsyncClient(api_key, api_password, base_url)

    async def close(self):
        await self._client.close()

    @property
    def products(self) -> _ProductsAPIAsync:
        return _ProductsAPIAsync(self._client)
