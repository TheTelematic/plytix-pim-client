from typing import Generator

import pytest

from plytix_pim_client.client import PlytixSync


@pytest.fixture(scope="session")
def plytix() -> Generator[PlytixSync, None, None]:
    _plytix = PlytixSync()
    yield _plytix
    _plytix.close()


@pytest.fixture(scope="session", autouse=True)
def setup(plytix: PlytixSync) -> None:
    yield

    _clean_up(plytix)
    plytix.close()


def _clean_up(plytix: PlytixSync) -> None:
    for products in plytix.products.search_all_products([[]], ["id"], [], "id"):
        plytix.products.delete_products([product.id for product in products])

    for attributes in plytix.products.attributes.search_all_product_attributes([[]], ["id"], [], "id"):
        plytix.products.attributes.delete_attributes([attribute.id for attribute in attributes])

    for families in plytix.products.families.search_all_families([[]], ["id"], [], "id"):
        plytix.products.families.delete_families([family.id for family in families])

    for asset in plytix.assets.search_all_assets([[]], ["id"], [], "id"):
        plytix.assets.delete_assets([asset.id for asset in asset])
