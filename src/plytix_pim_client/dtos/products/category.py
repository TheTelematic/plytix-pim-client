from dataclasses import dataclass

from plytix_pim_client.dtos.common.category import Category


@dataclass(frozen=True, slots=True, kw_only=True)
class ProductCategory(Category):
    ...  # fmt: skip
