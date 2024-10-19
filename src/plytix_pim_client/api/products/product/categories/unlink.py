import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPMethod, HTTPStatus
from typing import Tuple

import httpx

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.request import PlytixRequest


class ProductCategoryUnlinkAPI:
    @staticmethod
    def get_request(
        product_id: str,
        product_category_id: str,
    ) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.DELETE,
            endpoint=f"api/v1/products/{product_id}/categories/{product_category_id}",
        )

    @staticmethod
    def process_response(response: httpx.Response) -> bool:
        if response.status_code in [
            HTTPStatus.NOT_FOUND,
        ]:
            return False

        return True


class ProductCategoryUnlinkAPISyncMixin(BaseAPISyncMixin):
    def unlink_product_to_category(
        self,
        product_id: str,
        product_category_id: str,
    ) -> bool:
        """
        Unlink product from a category.

        :return: If unlinked successfully.
        """
        request = ProductCategoryUnlinkAPI.get_request(product_id, product_category_id)
        response = self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductCategoryUnlinkAPI.process_response(response)

    def unlink_product_to_categories(self, product_ids_and_category_ids: list[Tuple[str, str]]) -> list[bool]:
        """
        Unlink multiple products from categories. This uses threading to make the requests concurrently.

        :return: If unlinked successfully each.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.unlink_product_to_category, product_id, product_category_id)
                for product_id, product_category_id in product_ids_and_category_ids
            ]
            return [future.result() for future in futures]


class ProductCategoryUnlinkAPIAsyncMixin(BaseAPIAsyncMixin):
    async def unlink_product_to_category(
        self,
        product_id: str,
        product_category_id: str,
    ) -> bool:
        """
        Unlink product from a category.

        :return: If unlinked successfully.
        """
        request = ProductCategoryUnlinkAPI.get_request(product_id, product_category_id)
        response = await self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductCategoryUnlinkAPI.process_response(response)

    async def unlink_product_to_categories(self, product_ids_and_category_ids: list[Tuple[str, str]]) -> list[bool]:
        """
        Unlink multiple products from categories. This uses asyncio to make the requests concurrently.

        :return: If unlinked successfully each.
        """
        return list(
            await asyncio.gather(
                *[
                    self.unlink_product_to_category(product_id, product_category_id)
                    for product_id, product_category_id in product_ids_and_category_ids
                ]
            )
        )
