import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.delete import DeleteResourceAPI


class ProductCategoryDeleteAPI(DeleteResourceAPI):
    endpoint_prefix = "/api/v1/categories/product"


class ProductCategoryDeleteAPISyncMixin(BaseAPISyncMixin):
    def delete_product_category(self, category_id: str) -> bool:
        """
        Delete a product category.

        :return: True if deleted, False if it didn't exist.
        """
        request = ProductCategoryDeleteAPI.get_request(category_id)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductCategoryDeleteAPI.process_response(response)

    def delete_product_categories(self, category_ids: list[str]) -> list[bool]:
        """
        Delete multiple product categories. This uses threading to make the requests concurrently.

        :return: List of boolean. True if deleted, False if it didn't exist.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.delete_product_category, category_id) for category_id in category_ids]
            return [future.result() for future in futures]


class ProductCategoryDeleteAPIAsyncMixin(BaseAPIAsyncMixin):
    async def delete_product_category(self, category_id: str) -> bool:
        """
        Delete a product category.

        :return: True if deleted, False if it didn't exist.
        """
        request = ProductCategoryDeleteAPI.get_request(category_id)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductCategoryDeleteAPI.process_response(response)

    async def delete_product_categories(self, category_ids: list[str]) -> list[bool]:
        """
        Delete multiple product categories. This uses asyncio to make the requests concurrently.

        :return: List of boolean. True if deleted, False if it didn't exist.
        """
        return list(await asyncio.gather(*[self.delete_product_category(category_id) for category_id in category_ids]))
