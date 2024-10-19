from dataclasses import dataclass

from plytix_pim_client.dtos.base import BaseDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class ProductRelationship(BaseDTO):
    id: str | None = None
    name: str | None = None
