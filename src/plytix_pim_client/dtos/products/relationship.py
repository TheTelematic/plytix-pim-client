from dataclasses import dataclass

from plytix_pim_client.dtos.base import BaseDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class ProductRelationship(BaseDTO):
    id: str | None = None
    name: str | None = None
    label: str | None = None
    created_at: str | None = None
    modified_at: str | None = None
