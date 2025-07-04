from typing import AsyncGenerator, Generator, List, cast

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.search import SearchResourceAPI
from plytix_pim_client.constants import DEFAULT_PAGE_SIZE
from plytix_pim_client.dtos.assets.category import AssetCategory
from plytix_pim_client.dtos.filters import RelationshipSearchFilter, SearchFilter
from plytix_pim_client.dtos.pagination import Pagination
from plytix_pim_client.dtos.response import SearchResponse


class AssetCategoriesSearchAPI(SearchResourceAPI):
    endpoint = "/api/v1/categories/file/search"
    resource_dto_class = AssetCategory


class AssetCategoriesSearchAPISyncMixin(BaseAPISyncMixin):
    def search_asset_categories(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        pagination: Pagination,
        *,
        extra: dict = {},
    ) -> SearchResponse[AssetCategory]:
        """
        Search for asset categories matching the filters.

        :return: The asset categories found.
        """
        request = AssetCategoriesSearchAPI.get_request(filters, attributes, relationship_filters, pagination)
        response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return AssetCategoriesSearchAPI.process_search_response(
            response,
            **{k: v for k in {"return_pagination", "return_undocumented_data"} if ((v := extra.get(k)) is not None)},
        )

    def search_all_asset_categories(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Generator[List[AssetCategory], None, None]:
        """
        Iterate over all asset categories matching the filters.

        :return: The asset_categories found.
        """
        current_page = 1
        while True:
            pagination = Pagination(
                sort_by_attribute=sort_by_attribute,
                sort_ascending=sort_ascending,
                page_size=page_size,
                page=current_page,
            )
            asset_categories = cast(
                List[AssetCategory],
                self.search_asset_categories(filters, attributes, relationship_filters, pagination),
            )
            if not asset_categories:
                break
            yield asset_categories
            current_page += 1


class AssetCategoriesSearchAPIAsyncMixin(BaseAPIAsyncMixin):
    async def search_asset_categories(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        pagination: Pagination,
        *,
        extra: dict = {},
    ) -> SearchResponse[AssetCategory]:
        """
        Search for asset categories matching the filters.

        :return: The asset categories found.
        """
        request = AssetCategoriesSearchAPI.get_request(filters, attributes, relationship_filters, pagination)
        response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return AssetCategoriesSearchAPI.process_search_response(
            response,
            **{k: v for k in {"return_pagination", "return_undocumented_data"} if ((v := extra.get(k)) is not None)},
        )

    async def search_all_asset_categories(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> AsyncGenerator[List[AssetCategory], None]:
        """
        Iterate over all asset categories matching the filters.

        :return: The asset categories found.
        """
        current_page = 1
        while True:
            pagination = Pagination(
                sort_by_attribute=sort_by_attribute,
                sort_ascending=sort_ascending,
                page_size=page_size,
                page=current_page,
            )
            asset_categories = cast(
                List[AssetCategory],
                await self.search_asset_categories(filters, attributes, relationship_filters, pagination),
            )
            if not asset_categories:
                break
            yield asset_categories
            current_page += 1
