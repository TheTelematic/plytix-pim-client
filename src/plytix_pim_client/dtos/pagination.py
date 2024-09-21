from dataclasses import dataclass

from plytix_pim_client.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from plytix_pim_client.dtos.base import BaseDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class Pagination(BaseDTO):
    sort_by_attribute: str
    sort_ascending: bool = True
    page: int = 1
    page_size: int = DEFAULT_PAGE_SIZE

    def __post_init__(self):
        if self.page < 1:
            raise ValueError("Page must be greater than 0")
        if self.page_size < 1:
            raise ValueError("Page size must be greater than 0")
        if self.page_size > MAX_PAGE_SIZE:
            raise ValueError(f"Page size must be less than or equal to {MAX_PAGE_SIZE}")
        if not isinstance(self.sort_ascending, bool):
            raise ValueError("Sort ascending must be a boolean")
