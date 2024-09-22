from typing import List, Generator, AsyncGenerator

from plytix_pim_client.api.base import BaseAPISyncMixin, BaseAPIAsyncMixin
from plytix_pim_client.api.common.search import SearchResourceAPI
from plytix_pim_client.constants import DEFAULT_PAGE_SIZE
from plytix_pim_client.dtos.filters import SearchFilter, RelationshipSearchFilter
from plytix_pim_client.dtos.pagination import Pagination
from plytix_pim_client.dtos.products.attribute import ProductAttribute


class ProductAttributesSearchAPI(SearchResourceAPI):
    endpoint = "/api/v1/attributes/product/search"
    resource_dto_class = ProductAttribute


class ProductAttributesSearchAPISyncMixin(BaseAPISyncMixin):
    def search_product_attributes(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[RelationshipSearchFilter],
        pagination: Pagination,
    ) -> List[ProductAttribute]:
        """
        Search for products matching the filters.

        :return: The products found.
        """
        request = ProductAttributesSearchAPI.get_request(filters, attributes, relationship_filters, pagination)
        response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductAttributesSearchAPI.process_response(response)

    def search_all_product_attributes(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[RelationshipSearchFilter],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Generator[List[ProductAttribute], None, None]:
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
            products = self.search_product_attributes(filters, attributes, relationship_filters, pagination)
            if not products:
                break
            yield products
            current_page += 1


class ProductAttributesSearchAPIAsyncMixin(BaseAPIAsyncMixin):
    async def search_product_attributes(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[RelationshipSearchFilter],
        pagination: Pagination,
    ) -> List[ProductAttribute]:
        """
        Search for products matching the filters.

        :return: The products found.
        """
        request = ProductAttributesSearchAPI.get_request(filters, attributes, relationship_filters, pagination)
        response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductAttributesSearchAPI.process_response(response)

    async def search_all_product_attributes(
        self,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[RelationshipSearchFilter],
        sort_by_attribute: str,
        sort_ascending: bool = True,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> AsyncGenerator[List[ProductAttribute], None]:
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
            products = await self.search_product_attributes(filters, attributes, relationship_filters, pagination)
            if not products:
                break
            yield products
            current_page += 1
