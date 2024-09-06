import httpx

from plytix_pim_client.dtos.product import Product
from plytix_pim_client.http.async_ import AsyncClient
from plytix_pim_client.http.sync import SyncClient


class ProductsAPI:
    @staticmethod
    def _process_create_product_response(response: httpx.Response) -> Product:
        return Product.from_dict(response.json()["data"][0])


class ProductsAPISync(ProductsAPI):
    def __init__(self, client: SyncClient):
        self.client = client

    def create_product(self, product: Product) -> Product:
        response = self.client.make_request(self.client.method.POST, "/api/v1/products", json=product.clean_dict())
        return self._process_create_product_response(response)


class ProductsAPIAsync(ProductsAPI):
    def __init__(self, client: AsyncClient):
        self.client = client

    async def create_product(self, product: Product) -> Product:
        response = await self.client.make_request(
            self.client.method.POST, "/api/v1/products", json=product.clean_dict()
        )
        return self._process_create_product_response(response)
