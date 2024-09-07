from dataclasses import dataclass

from plytix_pim_client.dtos.base import BaseDto


@dataclass(frozen=True, slots=True, kw_only=True)
class Pagination(BaseDto):
    sort_by_attribute: str
    sort_ascending: bool = True
    page: int
    page_size: int
