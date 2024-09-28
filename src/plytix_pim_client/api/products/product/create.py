import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from typing import TypedDict

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.create import CreateResourceAPI
from plytix_pim_client.dtos.products.product import Product


class CreateProductDict(TypedDict):
    sku: str
    label: str | None


class ProductCreateAPI(CreateResourceAPI):
    endpoint = "/api/v1/products"
    resource_dto_class = Product


class ProductCreateAPISyncMixin(BaseAPISyncMixin):
    def create_product(self, sku: str, label: str | None = None) -> Product:
        """
        Create a product.

        :return: The product created.
        """
        data = {"sku": sku}
        if label:
            data["label"] = label

        request = ProductCreateAPI.get_request(**data)
        response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductCreateAPI.process_response(response)

    def create_products(self, products: list[CreateProductDict]) -> list[Product]:
        """
        Create multiple products. This uses threading to make the requests concurrently.

        :return: The products created.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.create_product, **product) for product in products]
            return [future.result() for future in futures]


class ProductCreateAPIAsyncMixin(BaseAPIAsyncMixin):
    async def create_product(self, sku: str, label: str | None = None) -> Product:
        """
        Create a product.

        :return: The product created.
        """
        data = {"sku": sku}
        if label:
            data["label"] = label

        request = ProductCreateAPI.get_request(**data)
        response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductCreateAPI.process_response(response)

    async def create_products(self, products: list[CreateProductDict]) -> list[Product]:
        """
        Create multiple products. This uses asyncio to make the requests concurrently.

        :return: The products created.
        """
        return list(await asyncio.gather(*[self.create_product(**product) for product in products]))
