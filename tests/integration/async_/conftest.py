from typing import AsyncGenerator

import pytest

from plytix_pim_client.client import PlytixAsync


@pytest.fixture(scope="session")
async def plytix() -> AsyncGenerator[PlytixAsync, None]:
    _plytix = PlytixAsync()
    yield _plytix
    await _plytix.close()


@pytest.fixture(scope="session", autouse=True)
async def setup(plytix: PlytixAsync) -> None:
    yield

    await _clean_up(plytix)
    await plytix.close()


async def _clean_up(plytix: PlytixAsync) -> None:
    async for products in plytix.products.search_all_products([[]], ["id"], [], "id"):
        await plytix.products.delete_products([product.id for product in products])

    async for attributes in plytix.products.attributes.search_all_product_attributes([[]], ["id"], [], "id"):
        await plytix.products.attributes.delete_attributes([attribute.id for attribute in attributes])

    async for families in plytix.products.families.search_all_families([[]], ["id"], [], "id"):
        await plytix.products.families.delete_families([family.id for family in families])

    async for asset in plytix.assets.search_all_assets([[]], ["id"], [], "id"):
        await plytix.assets.delete_assets([asset.id for asset in asset])
