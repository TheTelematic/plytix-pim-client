from dataclasses import dataclass

from plytix_pim_client.dtos.base import BaseDto


@dataclass(frozen=True, slots=True, kw_only=True)
class Family(BaseDto):
    created: str
    created_at: str
    id: str
    modified: str
    name: str
    total_attributes: int
    total_models: int
    total_products: int
    created_user_audit: dict
    modified_user_audit: dict
