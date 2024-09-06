from dataclasses import dataclass, field

from plytix_pim_client.dtos.base import BaseDto


@dataclass(frozen=True, slots=True, kw_only=True)
class Product(BaseDto):
    sku: str
    label: str | None = None
    _parent_id: str | None = None
    assets: list | None = field(default_factory=list)
    attributes: dict | None = field(default_factory=dict)
    categories: list | None = field(default_factory=list)
    created: str | None = None
    id: str | None = None
    modified: str | None = None
    num_variations: int | None = None
    status: str | None = None
    thumbnail: str | None = None
    created_user_audit: dict | None = field(default_factory=dict)
    modified_user_audit: dict | None = field(default_factory=dict)
    overwritten_attributes: dict | None = field(default_factory=dict)
    product_family_id: str | None = None
    product_family_model_id: str | None = None
    product_type: str | None = None
    relationships: list | None = field(default_factory=list)
