from dataclasses import dataclass

from plytix_pim_client.dtos.assets.asset import Asset


@dataclass(frozen=True, slots=True, kw_only=True)
class ProductAsset(Asset):
    ...  # fmt: skip
