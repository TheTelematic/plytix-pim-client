import asyncio
from datetime import datetime

import pytest


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def new_product_data() -> dict:
    now = datetime.now()
    return dict(
        sku=f"test-product-{now.isoformat()}",
        label=f"test_product_{str(now.timestamp()).replace('.', '')}",
    )


@pytest.fixture
def new_family_data() -> dict:
    now = datetime.now()
    return dict(
        name=f"test-family-{now.isoformat()}",
        attribute_ids=[],
        parent_attribute_ids=[],
    )
