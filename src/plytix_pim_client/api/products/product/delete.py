import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.delete import DeleteResourceAPI


class ProductDeleteAPI(DeleteResourceAPI):
    endpoint_prefix = "/api/v1/products"


class ProductDeleteAPISyncMixin(BaseAPISyncMixin):
    def delete_product(self, product_id: str) -> bool:
        """
        Delete a product.

        :return: True if deleted, False if it didn't exist.
        """
        request = ProductDeleteAPI.get_request(product_id)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductDeleteAPI.process_response(response)

    def delete_products(self, product_ids: list[str]) -> list[bool]:
        """
        Delete multiple products. This uses threading to make the requests concurrently.

        :return: List of boolean. True if deleted, False if it didn't exist.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.delete_product, product_id) for product_id in product_ids]
            return [future.result() for future in futures]


class ProductDeleteAPIAsyncMixin(BaseAPIAsyncMixin):
    async def delete_product(self, product_id: str) -> bool:
        """
        Delete a product.

        :return: True if deleted, False if it didn't exist.
        """
        request = ProductDeleteAPI.get_request(product_id)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductDeleteAPI.process_response(response)

    async def delete_products(self, product_ids: list[str]) -> list[bool]:
        """
        Delete multiple products. This uses asyncio to make the requests concurrently.

        :return: List of boolean. True if deleted, False if it didn't exist.
        """
        return list(await asyncio.gather(*[self.delete_product(product_id) for product_id in product_ids]))
