from typing import AsyncGenerator, Generator, List, cast

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.search import SearchResourceAPI
from plytix_pim_client.constants import DEFAULT_PAGE_SIZE
from plytix_pim_client.dtos.filters import RelationshipSearchFilter, SearchFilter
from plytix_pim_client.dtos.pagination import Pagination
from plytix_pim_client.dtos.products.family import ProductFamily
from plytix_pim_client.dtos.response import SearchResponse


class ProductFamilySearchAPI(SearchResourceAPI):
    endpoint = "/api/v1/product_families/search"
    resource_dto_class = ProductFamily


class ProductFamiliesSearchAPISyncMixin(BaseAPISyncMixin):
    def search_families(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        pagination: Pagination,
        *,
        extra: dict = {},
    ) -> SearchResponse[ProductFamily]:
        """
        Search for families matching the filters.

        :return: The families found.
        """
        request = ProductFamilySearchAPI.get_request(filters, attributes, relationship_filters, pagination)
        response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductFamilySearchAPI.process_search_response(
            response,
            **{k: v for k in {"return_pagination", "return_undocumented_data"} if ((v := extra.get(k)) is not None)},
        )

    def search_all_families(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Generator[List[ProductFamily], None, None]:
        """
        Iterate over all families matching the filters.

        :return: The families found.
        """
        current_page = 1
        while True:
            pagination = Pagination(
                sort_by_attribute=sort_by_attribute,
                sort_ascending=sort_ascending,
                page_size=page_size,
                page=current_page,
            )
            families = cast(
                List[ProductFamily],
                self.search_families(filters, attributes, relationship_filters, pagination),
            )
            if not families:
                break
            yield families
            current_page += 1


class ProductFamiliesSearchAPIAsyncMixin(BaseAPIAsyncMixin):
    async def search_families(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        pagination: Pagination,
        *,
        extra: dict = {},
    ) -> SearchResponse[ProductFamily]:
        """
        Search for families matching the filters.

        :return: The families found.
        """
        request = ProductFamilySearchAPI.get_request(filters, attributes, relationship_filters, pagination)
        response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductFamilySearchAPI.process_search_response(
            response,
            **{k: v for k in {"return_pagination", "return_undocumented_data"} if ((v := extra.get(k)) is not None)},
        )

    async def search_all_families(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> AsyncGenerator[List[ProductFamily], None]:
        """
        Iterate over all families matching the filters.

        :return: The families found.
        """
        current_page = 1
        while True:
            pagination = Pagination(
                sort_by_attribute=sort_by_attribute,
                sort_ascending=sort_ascending,
                page_size=page_size,
                page=current_page,
            )
            families = cast(
                List[ProductFamily],
                await self.search_families(filters, attributes, relationship_filters, pagination),
            )
            if not families:
                break
            yield families
            current_page += 1
