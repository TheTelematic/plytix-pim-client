from dataclasses import dataclass, field

from plytix_pim_client.dtos.base import BaseDto


@dataclass(frozen=True, slots=True, kw_only=True)
class Product(BaseDto):
    assets: list = field(default_factory=list)
    attributes: dict = field(default_factory=dict)
    categories: list = field(default_factory=list)
    created: str
    created_user_audit: dict
    id: str
    label: str
    modified: str
    modified_user_audit: dict
    num_variations: int
    overwritten_attributes: list = field(default_factory=list)
    product_family_id: str | None = None
    product_family_model_id: str | None = None
    product_type: str
    relationships: list = field(default_factory=list)
    sku: str
    status: str
