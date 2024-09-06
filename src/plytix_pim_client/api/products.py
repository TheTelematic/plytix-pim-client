from plytix_pim_client.dtos.product import Product
from plytix_pim_client.http.sync import SyncClient


class ProductsAPISync:
    def __init__(self, client: SyncClient):
        self.client = client

    def create_product(self, product: Product) -> Product:
        response = self.client.make_request(self.client.method.POST, "/api/v1/products", json=product.clean_dict())
        return Product.from_dict(response.json()["data"][0])
