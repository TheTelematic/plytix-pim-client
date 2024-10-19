from dataclasses import dataclass

from plytix_pim_client.dtos.base import BaseDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class ProductRelationship(BaseDTO):
    name: str | None = None
