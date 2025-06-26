from typing import AsyncGenerator, Generator, List, cast

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.search import SearchResourceAPI
from plytix_pim_client.constants import DEFAULT_PAGE_SIZE
from plytix_pim_client.dtos.assets.asset import Asset
from plytix_pim_client.dtos.filters import RelationshipSearchFilter, SearchFilter
from plytix_pim_client.dtos.pagination import Pagination
from plytix_pim_client.dtos.response import SearchResponse


class AssetsSearchAPI(SearchResourceAPI):
    endpoint = "/api/v1/assets/search"
    resource_dto_class = Asset


class AssetsSearchAPISyncMixin(BaseAPISyncMixin):
    def search_assets(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        pagination: Pagination,
        *,
        extra: dict = {},
    ) -> SearchResponse[Asset]:
        """
        Search for assets matching the filters.

        :return: The assets found.
        """
        request = AssetsSearchAPI.get_request(filters, attributes, relationship_filters, pagination)
        response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return AssetsSearchAPI.process_search_response(
            response,
            **{k: v for k in {"return_pagination", "return_undocumented_data"} if ((v := extra.get(k)) is not None)},
        )

    def search_all_assets(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Generator[List[Asset], None, None]:
        """
        Iterate over all assets matching the filters.

        :return: The assets found.
        """
        current_page = 1
        while True:
            pagination = Pagination(
                sort_by_attribute=sort_by_attribute,
                sort_ascending=sort_ascending,
                page_size=page_size,
                page=current_page,
            )
            assets = cast(List[Asset], self.search_assets(filters, attributes, relationship_filters, pagination))
            if not assets:
                break
            yield assets
            current_page += 1


class AssetsSearchAPIAsyncMixin(BaseAPIAsyncMixin):
    async def search_assets(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        pagination: Pagination,
        *,
        extra: dict = {},
    ) -> SearchResponse[Asset]:
        """
        Search for assets matching the filters.

        :return: The assets found.
        """
        request = AssetsSearchAPI.get_request(filters, attributes, relationship_filters, pagination)
        response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return AssetsSearchAPI.process_search_response(
            response,
            **{k: v for k in {"return_pagination", "return_undocumented_data"} if ((v := extra.get(k)) is not None)},
        )

    async def search_all_assets(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> AsyncGenerator[List[Asset], None]:
        """
        Iterate over all assets matching the filters.

        :return: The assets found.
        """
        current_page = 1
        while True:
            pagination = Pagination(
                sort_by_attribute=sort_by_attribute,
                sort_ascending=sort_ascending,
                page_size=page_size,
                page=current_page,
            )
            assets = cast(
                List[Asset],
                await self.search_assets(filters, attributes, relationship_filters, pagination),
            )
            if not assets:
                break
            yield assets
            current_page += 1
