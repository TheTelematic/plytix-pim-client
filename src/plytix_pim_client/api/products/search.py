from http import HTTPMethod
from typing import List, Generator, AsyncGenerator

import httpx

from plytix_pim_client.api.base import BaseAPISyncMixin, BaseAPIAsyncMixin
from plytix_pim_client.constants import DEFAULT_PAGE_SIZE
from plytix_pim_client.dtos.filters import ProductsSearchFilter, RelationshipSearchFilter
from plytix_pim_client.dtos.pagination import Pagination
from plytix_pim_client.dtos.product import Product
from plytix_pim_client.dtos.request import PlytixRequest


class ProductsSearchAPI:
    @staticmethod
    def get_search_products_request(
        filters: List[List[ProductsSearchFilter]],
        attributes: List[str],
        relationship_filters: List[RelationshipSearchFilter],
        pagination: Pagination,
    ) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.POST,
            endpoint="/api/v1/products/search",
            kwargs={
                "json": {
                    "filters": [[filter_.to_dict() for filter_ in filters_group] for filters_group in filters],
                    "attributes": attributes,
                    "relationship_filters": [filter_.to_dict() for filter_ in relationship_filters],
                    "pagination": {
                        "order": (
                            pagination.sort_by_attribute
                            if pagination.sort_ascending
                            else f"-{pagination.sort_by_attribute}"
                        ),
                        "page": pagination.page,
                        "page_size": pagination.page_size,
                    },
                }
            },
        )

    @staticmethod
    def process_search_products_response(response: httpx.Response) -> List[Product]:
        return [Product.from_dict(product) for product in response.json()["data"]]


class ProductsSearchAPISyncMixin(ProductsSearchAPI, BaseAPISyncMixin):
    def search_products(
        self,
        filters: List[List[ProductsSearchFilter]],
        attributes: List[str],
        relationship_filters: List[RelationshipSearchFilter],
        pagination: Pagination,
    ) -> List[Product]:
        """
        Search for products matching the filters in Plytix PIM.

        :return: The products found.
        """
        request = self.get_search_products_request(filters, attributes, relationship_filters, pagination)
        response = self.client.make_request(request.method, request.endpoint, **request.kwargs)
        return self.process_search_products_response(response)

    def search_all_products(
        self,
        filters: List[List[ProductsSearchFilter]],
        attributes: List[str],
        relationship_filters: List[RelationshipSearchFilter],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Generator[List[Product], None, None]:
        """
        Iterate over all products matching the filters in Plytix PIM.

        :return: The products found.
        """
        current_page = 1
        while True:
            pagination = Pagination(
                sort_by_attribute=sort_by_attribute,
                sort_ascending=sort_ascending,
                page_size=page_size,
                page=current_page,
            )
            products = self.search_products(filters, attributes, relationship_filters, pagination)
            if not products:
                break
            yield products
            current_page += 1


class ProductsSearchAPIAsyncMixin(ProductsSearchAPI, BaseAPIAsyncMixin):
    async def search_products(
        self,
        filters: List[List[ProductsSearchFilter]],
        attributes: List[str],
        relationship_filters: List[RelationshipSearchFilter],
        pagination: Pagination,
    ) -> List[Product]:
        """
        Search for products matching the filters in Plytix PIM.

        :return: The products found.
        """
        request = self.get_search_products_request(filters, attributes, relationship_filters, pagination)
        response = await self.client.make_request(request.method, request.endpoint, **request.kwargs)
        return self.process_search_products_response(response)

    async def search_all_products(
        self,
        filters: List[List[ProductsSearchFilter]],
        attributes: List[str],
        relationship_filters: List[RelationshipSearchFilter],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> AsyncGenerator[List[Product], None]:
        """
        Iterate over all products matching the filters in Plytix PIM.

        :return: The products found.
        """
        current_page = 1
        while True:
            pagination = Pagination(
                sort_by_attribute=sort_by_attribute,
                sort_ascending=sort_ascending,
                page_size=page_size,
                page=current_page,
            )
            products = await self.search_products(filters, attributes, relationship_filters, pagination)
            if not products:
                break
            yield products
            current_page += 1
