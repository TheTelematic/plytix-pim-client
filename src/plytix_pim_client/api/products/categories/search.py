from typing import AsyncGenerator, Generator, List

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.search import SearchResourceAPI
from plytix_pim_client.constants import DEFAULT_PAGE_SIZE
from plytix_pim_client.dtos.filters import RelationshipSearchFilter, SearchFilter
from plytix_pim_client.dtos.pagination import Pagination
from plytix_pim_client.dtos.products.category import ProductCategory


class ProductCategoriesSearchAPI(SearchResourceAPI):
    endpoint = "/api/v1/categories/product/search"
    resource_dto_class = ProductCategory


class ProductCategoriesSearchAPISyncMixin(BaseAPISyncMixin):
    def search_product_categories(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[RelationshipSearchFilter],
        pagination: Pagination,
    ) -> List[ProductCategory]:
        """
        Search for product categories matching the filters.

        :return: The product categories found.
        """
        request = ProductCategoriesSearchAPI.get_request(filters, attributes, relationship_filters, pagination)
        response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductCategoriesSearchAPI.process_response(response)

    def search_all_product_categories(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[RelationshipSearchFilter],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Generator[List[ProductCategory], None, None]:
        """
        Iterate over all product categories matching the filters.

        :return: The product_categories found.
        """
        current_page = 1
        while True:
            pagination = Pagination(
                sort_by_attribute=sort_by_attribute,
                sort_ascending=sort_ascending,
                page_size=page_size,
                page=current_page,
            )
            product_categories = self.search_product_categories(filters, attributes, relationship_filters, pagination)
            if not product_categories:
                break
            yield product_categories
            current_page += 1


class ProductCategoriesSearchAPIAsyncMixin(BaseAPIAsyncMixin):
    async def search_product_categories(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[RelationshipSearchFilter],
        pagination: Pagination,
    ) -> List[ProductCategory]:
        """
        Search for product categories matching the filters.

        :return: The product categories found.
        """
        request = ProductCategoriesSearchAPI.get_request(filters, attributes, relationship_filters, pagination)
        response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductCategoriesSearchAPI.process_response(response)

    async def search_all_product_categories(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[RelationshipSearchFilter],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> AsyncGenerator[List[ProductCategory], None]:
        """
        Iterate over all product categories matching the filters.

        :return: The product categories found.
        """
        current_page = 1
        while True:
            pagination = Pagination(
                sort_by_attribute=sort_by_attribute,
                sort_ascending=sort_ascending,
                page_size=page_size,
                page=current_page,
            )
            product_categories = await self.search_product_categories(
                filters, attributes, relationship_filters, pagination
            )
            if not product_categories:
                break
            yield product_categories
            current_page += 1
