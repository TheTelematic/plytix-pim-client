from typing import AsyncGenerator

import pytest

from plytix_pim_client.client import PlytixAsync
from plytix_pim_client.dtos.assets.asset import Asset
from plytix_pim_client.dtos.assets.category import AssetCategory
from plytix_pim_client.dtos.products.attribute import ProductAttribute, ProductAttributeTypeClass
from plytix_pim_client.dtos.products.category import ProductCategory
from plytix_pim_client.dtos.products.product import Product
from plytix_pim_client.dtos.products.relationship import ProductRelationship
from plytix_pim_client.dtos.products.variant import ProductVariant


@pytest.fixture()
async def plytix() -> AsyncGenerator[PlytixAsync, None]:
    _plytix = PlytixAsync(response_cooldown_seconds=2.0)
    yield _plytix
    await _plytix.close()


@pytest.fixture(autouse=True)
async def setup(plytix: PlytixAsync) -> AsyncGenerator[None, None]:
    yield

    plytix._client._response_cooldown_seconds = 0.0
    await _clean_up(plytix)
    await plytix.close()


async def _clean_up(plytix: PlytixAsync) -> None:
    async for products in plytix.products.search_all_products([], ["id"], [], "id"):
        for product in products:
            if product.id:
                variants = await plytix.products.variants.get_product_variants(product.id)
                if variants:
                    await plytix.products.delete_products([variant.id for variant in variants if variant.id])

                await plytix.products.delete_product(product.id)

    async for attributes in plytix.products.attributes.search_all_product_attributes([], ["id"], [], "id"):
        await plytix.products.attributes.delete_attributes([attribute.id for attribute in attributes if attribute.id])

    async for groups in plytix.products.attributes.groups.search_all_product_attributes_groups([], ["id"], [], "id"):
        await plytix.products.attributes.groups.delete_attributes_groups([group.id for group in groups if group.id])

    async for product_categories in plytix.products.categories.search_all_product_categories([], ["id"], [], "id"):
        await plytix.products.categories.delete_product_categories(
            [category.id for category in product_categories if category.id]
        )

    async for families in plytix.products.families.search_all_families([], ["id", "name"], [], "id"):
        await plytix.products.families.delete_families([family.id for family in families if family.id])

    async for relationships in plytix.products.relationships.search_all_product_relationships([], ["id"], [], "id"):
        await plytix.products.relationships.delete_product_relationships(
            [relationship.id for relationship in relationships if relationship.id]
        )

    async for assets in plytix.assets.search_all_assets([], ["id"], [], "id"):
        await plytix.assets.delete_assets([asset.id for asset in assets if asset.id])

    async for asset_categories in plytix.assets.categories.search_all_asset_categories([], ["id"], [], "id"):
        await plytix.assets.categories.delete_asset_categories(
            [category.id for category in asset_categories if category.id]
        )


# Fixtures
@pytest.fixture
async def product(plytix, new_product_data) -> Product:
    return await plytix.products.create_product(**new_product_data)


@pytest.fixture
async def product_attribute(plytix, new_product_attribute_data) -> ProductAttribute:
    return await plytix.products.attributes.create_attribute(**new_product_attribute_data)


@pytest.fixture
async def product_attribute_media(plytix, new_product_attribute_data) -> ProductAttribute:
    new_product_attribute_data["type_class"] = ProductAttributeTypeClass.MEDIA
    return await plytix.products.attributes.create_attribute(**new_product_attribute_data)


@pytest.fixture
async def product_category(plytix, new_product_category_data) -> ProductCategory:
    return await plytix.products.categories.create_product_category(**new_product_category_data)


@pytest.fixture
async def product_relationship(plytix, new_product_relationship_data) -> ProductRelationship:
    return await plytix.products.relationships.create_product_relationship(**new_product_relationship_data)


@pytest.fixture
async def product_related(plytix, product, product_relationship, new_product_data) -> Product:
    new_product_data["sku"] = f"{new_product_data['sku']}-related"
    related_product = await plytix.products.create_product(**new_product_data)
    assert related_product.id is not None
    await plytix.products.relationships.link_product_to_relationship(
        product.id, product_relationship.id, [{"product_id": related_product.id, "quantity": 1}]
    )
    return Product.from_dict(related_product.to_dict())


@pytest.fixture
async def product_variant(plytix, product, new_product_data) -> ProductVariant:
    new_product_data["sku"] = f"{new_product_data['sku']}-variant"
    variant = await plytix.products.create_product(**new_product_data)
    await plytix.products.variants.link_variant_to_product(product.id, variant.id)
    return ProductVariant.from_dict(variant.to_dict())


@pytest.fixture
async def asset_category(plytix, new_product_category_data) -> AssetCategory:
    return await plytix.assets.categories.create_asset_category(**new_product_category_data)


@pytest.fixture
async def product_subcategory(plytix, new_product_category_data, product_category) -> ProductCategory:
    new_product_category_data["name"] = f"{new_product_category_data['name']}-sub"
    return await plytix.products.categories.create_product_category(
        parent_category_id=product_category.id, **new_product_category_data
    )


@pytest.fixture
async def asset_subcategory(plytix, new_asset_category_data, asset_category) -> AssetCategory:
    new_asset_category_data["name"] = f"{new_asset_category_data['name']}-sub"
    return await plytix.assets.categories.create_asset_category(
        parent_category_id=asset_category.id, **new_asset_category_data
    )


@pytest.fixture
async def asset(plytix, new_asset_data_from_url_factory) -> Asset:
    return await plytix.assets.create_asset_by_url(**new_asset_data_from_url_factory())
