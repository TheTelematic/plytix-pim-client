from plytix_pim_client.api.products import ProductsAPISync
from plytix_pim_client.http.sync import SyncClient


class PlytixPimClientSync:
    def __init__(self, api_key: str | None = None, api_password: str | None = None, base_url: str | None = None):
        self._client = SyncClient(api_key, api_password, base_url)

    def close(self):
        self._client.close()

    @property
    def products(self) -> ProductsAPISync:
        return ProductsAPISync(self._client)
