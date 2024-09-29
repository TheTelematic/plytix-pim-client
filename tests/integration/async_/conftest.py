from typing import AsyncGenerator

import pytest

from plytix_pim_client.client import PlytixAsync


@pytest.fixture(scope="session")
async def plytix() -> AsyncGenerator[PlytixAsync, None]:
    _plytix = PlytixAsync()
    yield _plytix
    await _plytix.close()


@pytest.fixture(scope="session", autouse=True)
async def setup(plytix: PlytixAsync) -> AsyncGenerator[None, None]:
    yield

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
