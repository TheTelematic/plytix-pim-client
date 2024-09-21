from dataclasses import dataclass, field

from plytix_pim_client.dtos.base import BaseDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class Product(BaseDTO):
    assets: list = field(default_factory=list)
    attributes: dict = field(default_factory=dict)
    categories: list = field(default_factory=list)
    created: str | None = None
    created_user_audit: dict | None = field(default_factory=dict)
    id: str | None = None
    label: str | None = None
    modified: str | None = None
    modified_user_audit: dict | None = field(default_factory=dict)
    num_variations: int | None = None
    overwritten_attributes: list = field(default_factory=list)
    product_family_id: str | None = None
    product_family_model_id: str | None = None
    product_type: str | None = None
    relationships: list = field(default_factory=list)
    sku: str | None = None
    status: str | None = None
    thumbnail: str | None = None
