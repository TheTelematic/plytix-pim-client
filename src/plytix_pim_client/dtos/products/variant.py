from dataclasses import dataclass

from plytix_pim_client.dtos.products.product import Product


@dataclass(frozen=True, slots=True, kw_only=True)
class ProductVariant(Product):
    ...  # fmt: skip
