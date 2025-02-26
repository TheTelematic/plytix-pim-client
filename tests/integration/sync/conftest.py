from typing import Generator

import pytest

from plytix_pim_client.client import PlytixSync
from plytix_pim_client.dtos.assets.asset import Asset
from plytix_pim_client.dtos.assets.category import AssetCategory
from plytix_pim_client.dtos.products.attribute import ProductAttribute, ProductAttributeTypeClass
from plytix_pim_client.dtos.products.category import ProductCategory
from plytix_pim_client.dtos.products.product import Product
from plytix_pim_client.dtos.products.relationship import ProductRelationship
from plytix_pim_client.dtos.products.variant import ProductVariant


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
        for product in products:
            if product.id:
                variants = plytix.products.variants.get_product_variants(product.id)
                if variants:
                    plytix.products.delete_products([variant.id for variant in variants if variant.id])

                plytix.products.delete_product(product.id)

    for attributes in plytix.products.attributes.search_all_product_attributes([], ["id"], [], "id"):
        plytix.products.attributes.delete_attributes([attribute.id for attribute in attributes if attribute.id])

    for groups in plytix.products.attributes.groups.search_all_product_attributes_groups([], ["id"], [], "id"):
        plytix.products.attributes.groups.delete_attributes_groups([group.id for group in groups if group.id])

    for product_categories in plytix.products.categories.search_all_product_categories([], ["id"], [], "id"):
        plytix.products.categories.delete_product_categories(
            [category.id for category in product_categories if category.id]
        )

    for families in plytix.products.families.search_all_families([], ["id", "name"], [], "id"):
        plytix.products.families.delete_families([family.id for family in families if family.id])

    for relationships in plytix.products.relationships.search_all_product_relationships([], ["id"], [], "id"):
        plytix.products.relationships.delete_product_relationships(
            [relationship.id for relationship in relationships if relationship.id]
        )

    for assets in plytix.assets.search_all_assets([], ["id"], [], "id"):
        plytix.assets.delete_assets([asset.id for asset in assets if asset.id])

    for asset_categories in plytix.assets.categories.search_all_asset_categories([], ["id"], [], "id"):
        plytix.assets.categories.delete_asset_categories([category.id for category in asset_categories if category.id])


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
def product_relationship(plytix, new_product_relationship_data) -> ProductRelationship:
    return plytix.products.relationships.create_product_relationship(**new_product_relationship_data)


@pytest.fixture
def product_related(plytix, product, product_relationship, new_product_data) -> Product:
    new_product_data["sku"] = f"{new_product_data['sku']}-related"
    related_product = plytix.products.create_product(**new_product_data)
    assert related_product.id is not None
    plytix.products.relationships.link_product_to_relationship(
        product.id, product_relationship.id, [{"product_id": related_product.id, "quantity": 1}]
    )
    return Product.from_dict(related_product.to_dict())


@pytest.fixture
def product_variant(plytix, product, new_product_data) -> ProductVariant:
    new_product_data["sku"] = f"{new_product_data['sku']}-variant"
    variant = plytix.products.create_product(**new_product_data)
    plytix.products.variants.link_variant_to_product(product.id, variant.id)
    return ProductVariant.from_dict(variant.to_dict())


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
