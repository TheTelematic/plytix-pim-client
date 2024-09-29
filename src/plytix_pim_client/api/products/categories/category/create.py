import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPMethod
from typing import TypedDict

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.create import CreateResourceAPI
from plytix_pim_client.dtos.products.category import ProductCategory
from plytix_pim_client.dtos.request import PlytixRequest


class CreateProductCategoryDict(TypedDict):
    name: str
    parent_category_id: str | None


class ProductCategoryCreateAPI(CreateResourceAPI):
    endpoint = "/api/v1/categories/product"
    resource_dto_class = ProductCategory

    @classmethod
    def get_request(cls, **data) -> PlytixRequest:
        if data.get("parent_category_id"):
            endpoint = f"{cls.endpoint}/{data['parent_category_id']}"
        else:
            endpoint = cls.endpoint

        return PlytixRequest(
            method=HTTPMethod.POST,
            endpoint=endpoint,
            kwargs={"json": {"name": data["name"]}},
        )


class ProductCategoryCreateAPISyncMixin(BaseAPISyncMixin):
    def create_product_category(self, name: str, parent_category_id: str | None = None) -> ProductCategory:
        """
        Create a product category.

        :return: The product category created.
        """
        request = ProductCategoryCreateAPI.get_request(name=name, parent_category_id=parent_category_id)
        response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductCategoryCreateAPI.process_response(response)

    def create_product_categories(self, product_categories: list[CreateProductCategoryDict]) -> list[ProductCategory]:
        """
        Create multiple product categories. This uses threading to make the requests concurrently.

        :return: The product categories created.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.create_product_category, **category) for category in product_categories]
            return [future.result() for future in futures]


class ProductCategoryCreateAPIAsyncMixin(BaseAPIAsyncMixin):
    async def create_product_category(self, name: str, parent_category_id: str | None = None) -> ProductCategory:
        """
        Create a product category.

        :return: The product category created.
        """
        request = ProductCategoryCreateAPI.get_request(name=name, parent_category_id=parent_category_id)
        response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductCategoryCreateAPI.process_response(response)

    async def create_product_categories(
        self, product_categories: list[CreateProductCategoryDict]
    ) -> list[ProductCategory]:
        """
        Create multiple product categories. This uses asyncio to make the requests concurrently.

        :return: The product categories created.
        """
        return list(
            await asyncio.gather(*[self.create_product_category(**category) for category in product_categories])
        )
