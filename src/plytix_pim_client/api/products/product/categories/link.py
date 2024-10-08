from http import HTTPMethod, HTTPStatus
from typing import Tuple

import httpx

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.request import PlytixRequest


class ProductCategoryLinkAPI:
    @staticmethod
    def get_request(
        product_id: str,
        product_category_id: str,
    ) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.POST,
            endpoint=f"api/v1/products/{product_id}/categories",
            kwargs={"json": {"id": product_category_id}},
        )

    @staticmethod
    def process_response(response: httpx.Response) -> bool:
        if response.status_code in [
            HTTPStatus.NOT_FOUND,
        ]:
            return False

        return True


class ProductCategoryLinkAPISyncMixin(BaseAPISyncMixin):
    def link_product_to_category(
        self,
        product_id: str,
        product_category_id: str,
    ) -> bool:
        """
        Link product to a category.

        :return: If linked successfully.
        """
        request = ProductCategoryLinkAPI.get_request(product_id, product_category_id)
        response = self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductCategoryLinkAPI.process_response(response)

    def link_product_to_categories(self, product_ids_and_category_ids: list[Tuple[str, str]]) -> list[bool]:
        """
        Link multiple products to categories.
        This NOT uses threading to make the requests concurrently, due to race condition on server side.

        :return: If linked successfully each.
        """
        return [
            self.link_product_to_category(product_id, product_category_id)
            for product_id, product_category_id in product_ids_and_category_ids
        ]


class ProductCategoryLinkAPIAsyncMixin(BaseAPIAsyncMixin):
    async def link_product_to_category(
        self,
        product_id: str,
        product_category_id: str,
    ) -> bool:
        """
        Link product to a category.

        :return: If linked successfully.
        """
        request = ProductCategoryLinkAPI.get_request(product_id, product_category_id)
        response = await self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductCategoryLinkAPI.process_response(response)

    async def link_product_to_categories(self, product_ids_and_category_ids: list[Tuple[str, str]]) -> list[bool]:
        """
        Link multiple products to categories.
        This NOT uses asyncio to make the requests concurrently, due to race condition on server side.

        :return: If linked successfully each.
        """
        return [
            await self.link_product_to_category(product_id, product_category_id)
            for product_id, product_category_id in product_ids_and_category_ids
        ]
