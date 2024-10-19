import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus, HTTPMethod
from typing import Tuple, List

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.products.category import ProductCategory
from plytix_pim_client.dtos.request import PlytixRequest


class ProductCategoriesGetAPI:
    @classmethod
    def get_request(cls, **data) -> PlytixRequest:
        if data.get("product_category_id"):
            endpoint = f"/api/v1/products/{data['product_id']}/categories/{data['product_category_id']}"
        else:
            endpoint = f"/api/v1/products/{data['product_id']}/categories"

        return PlytixRequest(
            method=HTTPMethod.GET,
            endpoint=endpoint,
        )

    @classmethod
    def process_response(cls, response) -> List[ProductCategory] | None:
        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        if data := response.json().get("data", []):
            return [ProductCategory.from_dict(item) for item in data]

        return []


class ProductCategoriesGetAPISyncMixin(BaseAPISyncMixin):
    def get_product_categories(
        self, product_id: str, product_category_id: str | None = None
    ) -> List[ProductCategory] | None:
        """
        Get a product category if given, otherwise, all are returned.

        :return: The product categories.
        """
        request = ProductCategoriesGetAPI.get_request(product_id=product_id, product_category_id=product_category_id)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductCategoriesGetAPI.process_response(response)

    def get_multiple_product_categories(
        self, product_ids_and_category_ids: list[Tuple[str, str | None]]
    ) -> List[List[ProductCategory] | None]:
        """
        Get the categories for multiple products. This uses threading to make the requests concurrently.

        :return: The product categories.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.get_product_categories, product_id, product_category_id)
                for product_id, product_category_id in product_ids_and_category_ids
            ]
            return [future.result() for future in futures]


class ProductCategoriesGetAPIAsyncMixin(BaseAPIAsyncMixin):
    async def get_product_categories(
        self, product_id: str, product_category_id: str | None = None
    ) -> List[ProductCategory] | None:
        """
        Get a product category if given, otherwise, all are returned.

        :return: The product categories.
        """
        request = ProductCategoriesGetAPI.get_request(product_id=product_id, product_category_id=product_category_id)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductCategoriesGetAPI.process_response(response)

    async def get_multiple_product_categories(
        self, product_ids_and_category_ids: list[Tuple[str, str | None]]
    ) -> List[List[ProductCategory] | None]:
        """
        Get the categories for multiple products. This uses threading to make the requests concurrently.

        :return: The product categories.
        """
        return list(
            await asyncio.gather(
                *[
                    self.get_product_categories(product_id, product_category_id)
                    for product_id, product_category_id in product_ids_and_category_ids
                ]
            )
        )
