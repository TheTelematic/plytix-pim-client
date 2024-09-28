from typing import AsyncGenerator

import pytest

from plytix_pim_client import OperatorEnum, SearchFilter
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
    async for products in plytix.products.search_all_products([[]], ["id"], [], "id"):
        await plytix.products.delete_products([product.id for product in products if product.id])

    async for attributes in plytix.products.attributes.search_all_product_attributes([[]], ["id"], [], "id"):
        await plytix.products.attributes.delete_attributes([attribute.id for attribute in attributes if attribute.id])

    async for families in plytix.products.families.search_all_families(
        [[SearchFilter(field="name", operator=OperatorEnum.EXISTS, value=True)]], ["id"], [], "id"
    ):
        await plytix.products.families.delete_families([family.id for family in families if family.id])

    async for asset in plytix.assets.search_all_assets([[]], ["id"], [], "id"):
        await plytix.assets.delete_assets([asset.id for asset in asset if asset.id])
