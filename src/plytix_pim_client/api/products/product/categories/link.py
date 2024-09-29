import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPMethod, HTTPStatus
from typing import Tuple

import httpx

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.products.category import ProductCategory
from plytix_pim_client.dtos.request import PlytixRequest


class ProductCategoryLinkAttributeAPI:
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
    def process_response(response: httpx.Response) -> ProductCategory | None:
        if response.status_code in [
            HTTPStatus.NOT_FOUND,
        ]:
            return None

        return ProductCategory.from_dict(response.json()["data"][0])


class ProductCategoryLinkAttributeAPISyncMixin(BaseAPISyncMixin):
    def link_product_to_category(
        self,
        product_id: str,
        product_category_id: str,
    ) -> ProductCategory | None:
        """
        Link product to a category.

        :return: If linked successfully.
        """
        request = ProductCategoryLinkAttributeAPI.get_request(product_id, product_category_id)
        response = self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductCategoryLinkAttributeAPI.process_response(response)

    def link_product_to_categories(
        self, product_ids_and_category_ids: list[Tuple[str, str]]
    ) -> list[ProductCategory | None]:
        """
        Link multiple products to categories. This uses threading to make the requests concurrently.

        :return: If linked successfully each.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.link_product_to_category, product_id, product_category_id)
                for product_id, product_category_id in product_ids_and_category_ids
            ]
            return [future.result() for future in futures]


class ProductCategoryLinkAttributeAPIAsyncMixin(BaseAPIAsyncMixin):
    async def link_product_to_category(
        self,
        product_id: str,
        product_category_id: str,
    ) -> ProductCategory | None:
        """
        Link product to a category.

        :return: If linked successfully.
        """
        request = ProductCategoryLinkAttributeAPI.get_request(product_id, product_category_id)
        response = await self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductCategoryLinkAttributeAPI.process_response(response)

    async def link_product_to_categories(
        self, product_ids_and_category_ids: list[Tuple[str, str]]
    ) -> list[ProductCategory | None]:
        """
        Link multiple products to categories. This uses asyncio to make the requests concurrently.

        :return: If linked successfully each.
        """
        return list(
            await asyncio.gather(
                *[
                    self.link_product_to_category(product_id, product_category_id)
                    for product_id, product_category_id in product_ids_and_category_ids
                ]
            )
        )
