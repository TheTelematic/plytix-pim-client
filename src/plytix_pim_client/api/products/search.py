from typing import AsyncGenerator, Generator, List, cast

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.search import SearchResourceAPI
from plytix_pim_client.constants import DEFAULT_PAGE_SIZE
from plytix_pim_client.dtos.filters import RelationshipSearchFilter, SearchFilter
from plytix_pim_client.dtos.pagination import Pagination
from plytix_pim_client.dtos.products.product import Product
from plytix_pim_client.dtos.response import SearchResponse


class ProductsSearchAPI(SearchResourceAPI):
    endpoint = "/api/v1/products/search"
    resource_dto_class = Product


class ProductsSearchAPISyncMixin(BaseAPISyncMixin):
    def search_products(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        pagination: Pagination,
        *,
        extra: dict = {},
    ) -> SearchResponse[Product]:
        """
        Search for products matching the filters.

        :return: The products found.
        """
        request = ProductsSearchAPI.get_request(filters, attributes, relationship_filters, pagination)
        response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductsSearchAPI.process_search_response(
            response,
            **{k: v for k in {"return_pagination", "return_undocumented_data"} if ((v := extra.get(k)) is not None)},
        )

    def search_all_products(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Generator[List[Product], None, None]:
        """
        Iterate over all products matching the filters.

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
            products = cast(List[Product], self.search_products(filters, attributes, relationship_filters, pagination))
            if not products:
                break
            yield products
            current_page += 1


class ProductsSearchAPIAsyncMixin(BaseAPIAsyncMixin):
    async def search_products(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        pagination: Pagination,
        *,
        extra: dict = {},
    ) -> SearchResponse[Product]:
        """
        Search for products matching the filters.

        :return: The products found.
        """
        request = ProductsSearchAPI.get_request(filters, attributes, relationship_filters, pagination)
        response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductsSearchAPI.process_search_response(
            response,
            **{k: v for k in {"return_pagination", "return_undocumented_data"} if ((v := extra.get(k)) is not None)},
        )

    async def search_all_products(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> AsyncGenerator[List[Product], None]:
        """
        Iterate over all products matching the filters.

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
            products = cast(
                List[Product],
                await self.search_products(filters, attributes, relationship_filters, pagination),
            )
            if not products:
                break
            yield products
            current_page += 1
