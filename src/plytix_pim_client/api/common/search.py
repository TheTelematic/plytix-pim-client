from http import HTTPMethod
from typing import Generic, List, TypeVar

import httpx

from plytix_pim_client.dtos.base import BaseDTO
from plytix_pim_client.dtos.filters import RelationshipSearchFilter, SearchFilter
from plytix_pim_client.dtos.pagination import Pagination
from plytix_pim_client.dtos.request import PlytixRequest
from plytix_pim_client.dtos.response import PaginationResponse, SearchResponse, SearchResponseWithPagination


T = TypeVar("T", bound=BaseDTO)


class SearchResourceAPI(Generic[T]):
    endpoint: str
    resource_dto_class: T

    @classmethod
    def get_request(
        cls,
        filters: List[List[SearchFilter]],
        attributes: List[str],
        relationship_filters: List[List[RelationshipSearchFilter]],
        pagination: Pagination,
    ) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.POST,
            endpoint=cls.endpoint,
            kwargs={
                "json": {
                    "filters": [[filter_.to_dict() for filter_ in filters_group] for filters_group in filters],
                    "attributes": attributes,
                    "relationship_filters": [
                        [filter_.to_dict() for filter_ in relationship_filters_group]
                        for relationship_filters_group in relationship_filters
                    ],
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

    @classmethod
    def _process_response_data(cls, data: List[dict], return_undocumented_data: bool) -> List[T]:
        return [
            cls.resource_dto_class.from_dict(item, include_undocumented=return_undocumented_data)
            for item in data
        ]

    @classmethod
    def process_response(cls, response: httpx.Response, return_undocumented_data: bool = True) -> List[T]:
        return cls._process_response_data(response.json(), return_undocumented_data)

    @classmethod
    def process_search_response(
        cls,
        response: httpx.Response,
        *,
        return_pagination: bool = False,
        return_undocumented_data: bool = True
    ) -> SearchResponse:
        json_response = response.json()
        data = cls._process_response_data(json_response["data"], return_undocumented_data)

        if return_pagination:
            return SearchResponseWithPagination(
                data=data,
                pagination=PaginationResponse(**json_response["pagination"]),
            )
        return data
