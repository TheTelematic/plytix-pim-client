from typing import AsyncGenerator, Generator, List, cast

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.search import SearchResourceAPI
from plytix_pim_client.constants import DEFAULT_PAGE_SIZE
from plytix_pim_client.dtos.filters import RelationshipSearchFilter, SearchFilter
from plytix_pim_client.dtos.pagination import Pagination
from plytix_pim_client.dtos.products.relationship import ProductRelationship
from plytix_pim_client.dtos.response import SearchResponse


class ProductRelationshipsSearchAPI(SearchResourceAPI):
    endpoint = "/api/v1/relationships/search"
    resource_dto_class = ProductRelationship


class ProductRelationshipsSearchAPISyncMixin(BaseAPISyncMixin):
    def search_product_relationships(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        pagination: Pagination,
        *,
        extra: dict = {},
    ) -> SearchResponse[ProductRelationship]:
        """
        Search for product relationships matching the filters.

        :return: The product relationships found.
        """
        request = ProductRelationshipsSearchAPI.get_request(filters, attributes, relationship_filters, pagination)
        response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductRelationshipsSearchAPI.process_search_response(
            response,
            **{k: v for k in {"return_pagination", "return_undocumented_data"} if ((v := extra.get(k)) is not None)},
        )

    def search_all_product_relationships(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Generator[List[ProductRelationship], None, None]:
        """
        Iterate over all product relationships matching the filters.

        :return: The product_relationships found.
        """
        current_page = 1
        while True:
            pagination = Pagination(
                sort_by_attribute=sort_by_attribute,
                sort_ascending=sort_ascending,
                page_size=page_size,
                page=current_page,
            )
            product_relationships = cast(
                List[ProductRelationship],
                self.search_product_relationships(filters, attributes, relationship_filters, pagination),
            )
            if not product_relationships:
                break
            yield product_relationships
            current_page += 1


class ProductRelationshipsSearchAPIAsyncMixin(BaseAPIAsyncMixin):
    async def search_product_relationships(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        pagination: Pagination,
        *,
        extra: dict = {},
    ) -> SearchResponse[ProductRelationship]:
        """
        Search for product relationships matching the filters.

        :return: The product relationships found.
        """
        request = ProductRelationshipsSearchAPI.get_request(filters, attributes, relationship_filters, pagination)
        response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductRelationshipsSearchAPI.process_search_response(
            response,
            **{k: v for k in {"return_pagination", "return_undocumented_data"} if ((v := extra.get(k)) is not None)},
        )

    async def search_all_product_relationships(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> AsyncGenerator[List[ProductRelationship], None]:
        """
        Iterate over all product relationships matching the filters.

        :return: The product relationships found.
        """
        current_page = 1
        while True:
            pagination = Pagination(
                sort_by_attribute=sort_by_attribute,
                sort_ascending=sort_ascending,
                page_size=page_size,
                page=current_page,
            )
            product_relationships = cast(
                List[ProductRelationship],
                await self.search_product_relationships(filters, attributes, relationship_filters, pagination),
            )
            if not product_relationships:
                break
            yield product_relationships
            current_page += 1
