import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPMethod, HTTPStatus

import httpx

from plytix_pim_client.api.base import BaseAPISyncMixin, BaseAPIAsyncMixin
from plytix_pim_client.dtos.request import PlytixRequest


class ProductDeleteAPI:
    @staticmethod
    def get_delete_product_request(product_id: str) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.DELETE,
            endpoint=f"/api/v1/products/{product_id}",
        )

    @staticmethod
    def process_delete_product_response(response: httpx.Response) -> bool:
        if response.status_code == HTTPStatus.NOT_FOUND:
            return False
        else:
            return True


class ProductDeleteAPISyncMixin(ProductDeleteAPI, BaseAPISyncMixin):
    def delete_product(self, product_id: str) -> bool:
        """
        Delete a product.

        :return: True if deleted, False if it didn't exist.
        """
        request = self.get_delete_product_request(product_id)
        response = self.client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return self.process_delete_product_response(response)

    def delete_products(self, product_ids: list[str]) -> list[bool]:
        """
        Delete multiple products. This uses threading to make the requests concurrently.

        :return: List of boolean. True if deleted, False if it didn't exist.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.delete_product, product_id) for product_id in product_ids]
            return [future.result() for future in futures]


class ProductDeleteAPIAsyncMixin(ProductDeleteAPI, BaseAPIAsyncMixin):
    async def delete_product(self, product_id: str) -> bool:
        """
        Delete a product.

        :return: True if deleted, False if it didn't exist.
        """
        request = self.get_delete_product_request(product_id)
        response = await self.client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return self.process_delete_product_response(response)

    async def delete_products(self, product_ids: list[str]) -> list[bool]:
        """
        Delete multiple products. This uses asyncio to make the requests concurrently.

        :return: List of boolean. True if deleted, False if it didn't exist.
        """
        return list(await asyncio.gather(*[self.delete_product(product_id) for product_id in product_ids]))
