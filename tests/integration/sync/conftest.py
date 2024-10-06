from typing import Generator

import pytest

from plytix_pim_client.client import PlytixSync
from plytix_pim_client.dtos.assets.asset import Asset
from plytix_pim_client.dtos.assets.category import AssetCategory
from plytix_pim_client.dtos.products.attribute import ProductAttribute, ProductAttributeTypeClass
from plytix_pim_client.dtos.products.category import ProductCategory
from plytix_pim_client.dtos.products.product import Product


@pytest.fixture()
def plytix() -> Generator[PlytixSync, None, None]:
    _plytix = PlytixSync(response_cooldown_seconds=2.0)
    yield _plytix
    _plytix.close()


@pytest.fixture(autouse=True)
def setup(plytix: PlytixSync) -> Generator[None, None, None]:
    yield

    plytix._client._response_cooldown_seconds = 0.0
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
def product_attribute(plytix, new_product_attribute_data) -> ProductAttribute:
    return plytix.products.attributes.create_attribute(**new_product_attribute_data)


@pytest.fixture
def product_attribute_media(plytix, new_product_attribute_data) -> ProductAttribute:
    new_product_attribute_data["type_class"] = ProductAttributeTypeClass.MEDIA
    return plytix.products.attributes.create_attribute(**new_product_attribute_data)


@pytest.fixture
def product_category(plytix, new_product_category_data) -> ProductCategory:
    return plytix.products.categories.create_product_category(**new_product_category_data)


@pytest.fixture
def asset_category(plytix, new_product_category_data) -> AssetCategory:
    return plytix.assets.categories.create_asset_category(**new_product_category_data)


@pytest.fixture
def product_subcategory(plytix, new_product_category_data, product_category) -> ProductCategory:
    new_product_category_data["name"] = f"{new_product_category_data['name']}-sub"
    return plytix.products.categories.create_product_category(
        parent_category_id=product_category.id, **new_product_category_data
    )


@pytest.fixture
def asset_subcategory(plytix, new_asset_category_data, asset_category) -> AssetCategory:
    new_asset_category_data["name"] = f"{new_asset_category_data['name']}-sub"
    return plytix.assets.categories.create_asset_category(
        parent_category_id=asset_category.id, **new_asset_category_data
    )


@pytest.fixture
def asset(plytix, new_asset_data_from_url_factory) -> Asset:
    return plytix.assets.create_asset_by_url(**new_asset_data_from_url_factory())
