from typing import AsyncGenerator

import pytest

from plytix_pim_client import Product
from plytix_pim_client.client import PlytixAsync
from plytix_pim_client.dtos.assets.asset import Asset
from plytix_pim_client.dtos.products.attribute import ProductAttribute
from plytix_pim_client.dtos.products.category import ProductCategory


@pytest.fixture(scope="session")
async def plytix() -> AsyncGenerator[PlytixAsync, None]:
    _plytix = PlytixAsync(response_cooldown_seconds=2.0)
    yield _plytix
    await _plytix.close()


@pytest.fixture(scope="session", autouse=True)
async def setup(plytix: PlytixAsync) -> AsyncGenerator[None, None]:
    yield

    plytix._client._response_cooldown_seconds = 0.0
    await _clean_up(plytix)
    await plytix.close()


async def _clean_up(plytix: PlytixAsync) -> None:
    async for products in plytix.products.search_all_products([], ["id"], [], "id"):
        await plytix.products.delete_products([product.id for product in products if product.id])

    async for attributes in plytix.products.attributes.search_all_product_attributes([], ["id"], [], "id"):
        await plytix.products.attributes.delete_attributes([attribute.id for attribute in attributes if attribute.id])

    async for families in plytix.products.families.search_all_families([], ["id", "name"], [], "id"):
        await plytix.products.families.delete_families([family.id for family in families if family.id])

    async for assets in plytix.assets.search_all_assets([], ["id"], [], "id"):
        await plytix.assets.delete_assets([asset.id for asset in assets if asset.id])

    async for asset_categories in plytix.assets.categories.search_all_asset_categories([], ["id"], [], "id"):
        await plytix.assets.categories.delete_asset_categories(
            [category.id for category in asset_categories if category.id]
        )

    async for product_categories in plytix.products.categories.search_all_product_categories([], ["id"], [], "id"):
        await plytix.products.categories.delete_product_categories(
            [category.id for category in product_categories if category.id]
        )


# Fixtures
@pytest.fixture
async def product(plytix, new_product_data) -> Product:
    return await plytix.products.create_product(**new_product_data)


@pytest.fixture
async def product_attribute(plytix, new_product_attribute_data) -> ProductAttribute:
    return await plytix.products.attributes.create_attribute(**new_product_attribute_data)


@pytest.fixture
async def product_category(plytix, new_product_category_data) -> ProductCategory:
    return await plytix.products.categories.create_product_category(**new_product_category_data)


@pytest.fixture
async def asset(plytix, new_asset_data_from_url_factory) -> Asset:
    return await plytix.assets.create_asset_by_url(**new_asset_data_from_url_factory())
