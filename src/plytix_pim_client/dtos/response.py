from dataclasses import dataclass
from typing import Generic, List, TypeVar, Union

from plytix_pim_client.dtos.base import BaseDTO


@dataclass
class PaginationResponse:
    count: int
    order: str | None
    page: int
    page_size: int
    total_count: int


T = TypeVar("T", bound=BaseDTO)


DataResponse = List[T]


@dataclass
class SearchResponseWithPagination(Generic[T]):
    data: DataResponse[T]
    pagination: PaginationResponse


SearchResponse = Union[DataResponse, SearchResponseWithPagination[T]]
