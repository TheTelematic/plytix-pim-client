from dataclasses import dataclass, field
from enum import StrEnum

from plytix_pim_client.dtos.base import BaseDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class ProductFamily(BaseDTO):
    created: str | None = None
    created_at: str | None = None
    id: str | None = None
    modified: str | None = None
    name: str | None = None
    total_attributes: int | None = None
    total_models: int | None = None
    total_products: int | None = None
    created_user_audit: dict | None = field(default_factory=dict)
    modified_user_audit: dict | None = field(default_factory=dict)


class ProductAttributeFamilyLevel(StrEnum):
    ON = "parent_level"
    OFF = "no_level"


@dataclass(frozen=True, slots=True, kw_only=True)
class ProductFamilyAttribute(BaseDTO):
    attribute_level: ProductAttributeFamilyLevel | None = None
    id: str | None = None
    label: str | None = None
    name: str | None = None