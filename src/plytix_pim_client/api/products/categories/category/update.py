import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus
from typing import Tuple

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.update import UpdateResourceAPI
from plytix_pim_client.dtos.products.category import ProductCategory


class ProductCategoryUpdateAPI(UpdateResourceAPI):
    endpoint_prefix = "/api/v1/categories/product"
    resource_dto_class = ProductCategory


class ProductCategoryUpdateAPISyncMixin(BaseAPISyncMixin):
    def convert_to_first_level_category(
        self,
        category_id: str,
    ) -> ProductCategory | None:
        """
        Convert a subcategory to a first level category.

        :return: The category.
        """
        request = ProductCategoryUpdateAPI.get_request(category_id, {"parent_id": ""})
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductCategoryUpdateAPI.process_response(response)

    def move_category(self, category_id: str, parent_id: str) -> ProductCategory | None:
        """
        Move a category to another category.

        :return: The category.
        """
        request = ProductCategoryUpdateAPI.get_request(category_id, {"parent_id": parent_id})
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductCategoryUpdateAPI.process_response(response)

    def sorting_category(self, category_id: str, subcategory_ids: list[str]) -> ProductCategory | None:
        """
        Sorting a category.

        :return: The category.
        """
        request = ProductCategoryUpdateAPI.get_request(category_id, {"sort_children": subcategory_ids})
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductCategoryUpdateAPI.process_response(response)

    def sorting_root_category(self, subcategory_ids: list[str]) -> None:
        """
        Sorting the root category.

        :return: The category.
        """
        request = ProductCategoryUpdateAPI.get_request("root", {"sort_children": subcategory_ids})
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        ProductCategoryUpdateAPI.process_response(response)

    def convert_to_first_level_categories(self, category_ids: list[str]) -> list[ProductCategory | None]:
        """
        Convert to first level multiple categories. This uses threading to make the requests concurrently.

        :return: The categories.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.convert_to_first_level_category, category_id) for category_id in category_ids
            ]
            return [future.result() for future in futures]

    def move_categories(self, category_ids_and_parent_ids: list[Tuple[str, str]]) -> list[ProductCategory | None]:
        """
        Move multiple categories. This uses threading to make the requests concurrently.

        :return: The categories.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.move_category, category_id, parent_id)
                for category_id, parent_id in category_ids_and_parent_ids
            ]
            return [future.result() for future in futures]


class ProductCategoryUpdateAPIAsyncMixin(BaseAPIAsyncMixin):
    async def convert_to_first_level_category(
        self,
        category_id: str,
    ) -> ProductCategory | None:
        """
        Convert a subcategory to a first level category.

        :return: The category.
        """
        request = ProductCategoryUpdateAPI.get_request(category_id, {"parent_id": ""})
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductCategoryUpdateAPI.process_response(response)

    async def move_category(self, category_id: str, parent_id: str) -> ProductCategory | None:
        """
        Move a category to another category.

        :return: The category.
        """
        request = ProductCategoryUpdateAPI.get_request(category_id, {"parent_id": parent_id})
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductCategoryUpdateAPI.process_response(response)

    async def sorting_category(self, category_id: str, subcategory_ids: list[str]) -> ProductCategory | None:
        """
        Sorting a category.

        :return: The category.
        """
        request = ProductCategoryUpdateAPI.get_request(category_id, {"sort_children": subcategory_ids})
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductCategoryUpdateAPI.process_response(response)

    async def sorting_root_category(self, subcategory_ids: list[str]) -> None:
        """
        Sorting the root category.

        :return: The category.
        """
        request = ProductCategoryUpdateAPI.get_request("root", {"sort_children": subcategory_ids})
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        ProductCategoryUpdateAPI.process_response(response)

    async def convert_to_first_level_categories(self, category_ids: list[str]) -> list[ProductCategory | None]:
        """
        Convert to first level multiple categories. This uses asyncio to make the requests concurrently.

        :return: The categories.
        """
        return list(
            await asyncio.gather(*[self.convert_to_first_level_category(category_id) for category_id in category_ids])
        )

    async def move_categories(self, category_ids_and_parent_ids: list[Tuple[str, str]]) -> list[ProductCategory | None]:
        """
        Move multiple categories. This uses asyncio to make the requests concurrently.

        :return: The categories.
        """
        return list(
            await asyncio.gather(
                *[self.move_category(category_id, parent_id) for category_id, parent_id in category_ids_and_parent_ids]
            )
        )
