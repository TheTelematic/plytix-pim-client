from typing import List, Generator, AsyncGenerator

from plytix_pim_client.api.base import BaseAPISyncMixin, BaseAPIAsyncMixin
from plytix_pim_client.api.common.search import SearchResourceAPI
from plytix_pim_client.constants import DEFAULT_PAGE_SIZE
from plytix_pim_client.dtos.family import Family
from plytix_pim_client.dtos.filters import SearchFilter, RelationshipSearchFilter
from plytix_pim_client.dtos.pagination import Pagination
from plytix_pim_client.dtos.product import Product


class FamilySearchAPI(SearchResourceAPI):
    endpoint = "/api/v1/product_families/search"
    resource_dto_class = Family


class FamiliesSearchAPISyncMixin(BaseAPISyncMixin):
    def search_families(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[RelationshipSearchFilter],
        pagination: Pagination,
    ) -> List[Product]:
        """
        Search for families matching the filters.

        :return: The families found.
        """
        request = FamilySearchAPI.get_request(filters, attributes, relationship_filters, pagination)
        response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return FamilySearchAPI.process_response(response)

    def search_all_families(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[RelationshipSearchFilter],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Generator[List[Product], None, None]:
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
            families = self.search_families(filters, attributes, relationship_filters, pagination)
            if not families:
                break
            yield families
            current_page += 1


class FamiliesSearchAPIAsyncMixin(BaseAPIAsyncMixin):
    async def search_families(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[RelationshipSearchFilter],
        pagination: Pagination,
    ) -> List[Product]:
        """
        Search for families matching the filters.

        :return: The families found.
        """
        request = FamilySearchAPI.get_request(filters, attributes, relationship_filters, pagination)
        response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return FamilySearchAPI.process_response(response)

    async def search_all_families(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[RelationshipSearchFilter],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> AsyncGenerator[List[Product], None]:
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
            families = await self.search_families(filters, attributes, relationship_filters, pagination)
            if not families:
                break
            yield families
            current_page += 1
