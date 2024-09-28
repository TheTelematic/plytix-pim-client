import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.get import GetResourceAPI
from plytix_pim_client.dtos.products.product import Product


class ProductGetAPI(GetResourceAPI):
    endpoint_prefix = "/api/v1/products"
    resource_dto_class = Product


class ProductGetAPISyncMixin(BaseAPISyncMixin):
    def get_product(self, product_id: str) -> Product | None:
        """
        Get a product.

        :return: The product.
        """
        request = ProductGetAPI.get_request(product_id)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductGetAPI.process_response(response)

    def get_products(self, product_ids: list[str]) -> list[Product | None]:
        """
        Get multiple products. This uses threading to make the requests concurrently.

        :return: The products.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.get_product, product_id) for product_id in product_ids]
            return [future.result() for future in futures]


class ProductGetAPIAsyncMixin(BaseAPIAsyncMixin):
    async def get_product(self, product_id: str) -> Product | None:
        """
        Get a product.

        :return: The product.
        """
        request = ProductGetAPI.get_request(product_id)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductGetAPI.process_response(response)

    async def get_products(self, product_ids: list[str]) -> list[Product | None]:
        """
        Get multiple products. This uses asyncio to make the requests concurrently.

        :return: The products.
        """
        return list(await asyncio.gather(*[self.get_product(product_id) for product_id in product_ids]))
