from dataclasses import dataclass

from plytix_pim_client.dtos.base import BaseDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class Category(BaseDTO):
    id: str | None = None
    modified: str | None = None
    n_children: int | None = None
    name: str | None = None
    order: str | None = None
    parents_ids: list[str] | None = None
    path: list[str] | None = None
    slug: str | None = None
