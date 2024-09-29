from typing import Generator

import pytest

from plytix_pim_client import Product
from plytix_pim_client.client import PlytixSync
from plytix_pim_client.dtos.products.category import ProductCategory


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
    for products in plytix.products.search_all_products([], ["id"], [], "id"):
        plytix.products.delete_products([product.id for product in products if product.id])

    for attributes in plytix.products.attributes.search_all_product_attributes([], ["id"], [], "id"):
        plytix.products.attributes.delete_attributes([attribute.id for attribute in attributes if attribute.id])

    for families in plytix.products.families.search_all_families([], ["id", "name"], [], "id"):
        plytix.products.families.delete_families([family.id for family in families if family.id])

    for assets in plytix.assets.search_all_assets([], ["id"], [], "id"):
        plytix.assets.delete_assets([asset.id for asset in assets if asset.id])

    for asset_categories in plytix.assets.categories.search_all_asset_categories([], ["id"], [], "id"):
        plytix.assets.categories.delete_asset_categories([category.id for category in asset_categories if category.id])

    for product_categories in plytix.products.categories.search_all_product_categories([], ["id"], [], "id"):
        plytix.products.categories.delete_product_categories(
            [category.id for category in product_categories if category.id]
        )


# Fixtures
@pytest.fixture
def product(plytix, new_product_data) -> Product:
    return plytix.products.create_product(**new_product_data)


@pytest.fixture
def product_category(plytix, new_product_category_data) -> ProductCategory:
    return plytix.products.categories.create_product_category(**new_product_category_data)
