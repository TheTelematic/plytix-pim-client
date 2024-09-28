from typing import Generator

import pytest

from plytix_pim_client import SearchFilter, OperatorEnum
from plytix_pim_client.client import PlytixSync


@pytest.fixture(scope="session")
def plytix() -> Generator[PlytixSync, None, None]:
    _plytix = PlytixSync()
    yield _plytix
    _plytix.close()


@pytest.fixture(scope="session", autouse=True)
def setup(plytix: PlytixSync) -> Generator[None, None, None]:
    yield

    _clean_up(plytix)
    plytix.close()


def _clean_up(plytix: PlytixSync) -> None:
    for products in plytix.products.search_all_products([[]], ["id"], [], "id"):
        plytix.products.delete_products([product.id for product in products if product.id])

    for attributes in plytix.products.attributes.search_all_product_attributes([[]], ["id"], [], "id"):
        plytix.products.attributes.delete_attributes([attribute.id for attribute in attributes if attribute.id])

    for families in plytix.products.families.search_all_families(
        [[SearchFilter(field="name", operator=OperatorEnum.EXISTS, value=True)]], ["id"], [], "id"
    ):
        plytix.products.families.delete_families([family.id for family in families if family.id])

    for asset in plytix.assets.search_all_assets([[]], ["id"], [], "id"):
        plytix.assets.delete_assets([asset.id for asset in asset if asset.id])
