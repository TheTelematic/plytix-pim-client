from http import HTTPMethod
from typing import List

import httpx

from plytix_pim_client.api.base import BaseAPISyncMixin, BaseAPIAsyncMixin
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
        request = self.get_search_products_request(filters, attributes, relationship_filters, pagination)
        response = self.client.make_request(request.method, request.endpoint, **request.kwargs)
        return self.process_search_products_response(response)


class ProductsSearchAPIAsyncMixin(ProductsSearchAPI, BaseAPIAsyncMixin):
    async def search_products(
        self,
        filters: List[List[ProductsSearchFilter]],
        attributes: List[str],
        relationship_filters: List[RelationshipSearchFilter],
        pagination: Pagination,
    ) -> List[Product]:
        request = self.get_search_products_request(filters, attributes, relationship_filters, pagination)
        response = await self.client.make_request(request.method, request.endpoint, **request.kwargs)
        return self.process_search_products_response(response)
