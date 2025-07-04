from typing import AsyncGenerator, Generator, List, cast

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.search import SearchResourceAPI
from plytix_pim_client.constants import DEFAULT_PAGE_SIZE
from plytix_pim_client.dtos.filters import RelationshipSearchFilter, SearchFilter
from plytix_pim_client.dtos.pagination import Pagination
from plytix_pim_client.dtos.products.attribute import ProductAttributesGroup
from plytix_pim_client.dtos.response import SearchResponse


class ProductAttributesGroupsSearchAPI(SearchResourceAPI):
    endpoint = "/api/v1/attribute-groups/product/search"
    resource_dto_class = ProductAttributesGroup


class ProductAttributesGroupsSearchAPISyncMixin(BaseAPISyncMixin):
    def search_product_attributes_groups(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        pagination: Pagination,
        *,
        extra: dict = {},
    ) -> SearchResponse[ProductAttributesGroup]:
        """
        Search for products attributes groups matching the filters.

        :return: The products attributes groups found.
        """
        request = ProductAttributesGroupsSearchAPI.get_request(filters, attributes, relationship_filters, pagination)
        response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductAttributesGroupsSearchAPI.process_search_response(
            response,
            **{k: v for k in {"return_pagination", "return_undocumented_data"} if ((v := extra.get(k)) is not None)},
        )

    def search_all_product_attributes_groups(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Generator[List[ProductAttributesGroup], None, None]:
        """
        Iterate over all products attributes groups matching the filters.

        :return: The products attributes groups found.
        """
        current_page = 1
        while True:
            pagination = Pagination(
                sort_by_attribute=sort_by_attribute,
                sort_ascending=sort_ascending,
                page_size=page_size,
                page=current_page,
            )
            products_attributes_groups = cast(
                List[ProductAttributesGroup],
                self.search_product_attributes_groups(filters, attributes, relationship_filters, pagination),
            )
            if not products_attributes_groups:
                break
            yield products_attributes_groups
            current_page += 1


class ProductAttributesGroupsSearchAPIAsyncMixin(BaseAPIAsyncMixin):
    async def search_product_attributes_groups(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        pagination: Pagination,
        *,
        extra: dict = {},
    ) -> SearchResponse[ProductAttributesGroup]:
        """
        Search for products attributes groups matching the filters.

        :return: The products attributes groups found.
        """
        request = ProductAttributesGroupsSearchAPI.get_request(filters, attributes, relationship_filters, pagination)
        response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductAttributesGroupsSearchAPI.process_search_response(
            response,
            **{k: v for k in {"return_pagination", "return_undocumented_data"} if ((v := extra.get(k)) is not None)},
        )

    async def search_all_product_attributes_groups(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> AsyncGenerator[List[ProductAttributesGroup], None]:
        """
        Iterate over all products attributes groups matching the filters.

        :return: The products attributes groups found.
        """
        current_page = 1
        while True:
            pagination = Pagination(
                sort_by_attribute=sort_by_attribute,
                sort_ascending=sort_ascending,
                page_size=page_size,
                page=current_page,
            )
            products_attributes_groups = cast(
                List[ProductAttributesGroup],
                await self.search_product_attributes_groups(filters, attributes, relationship_filters, pagination),
            )
            if not products_attributes_groups:
                break
            yield products_attributes_groups
            current_page += 1
