import asyncio
from datetime import datetime

import pytest

from plytix_pim_client.dtos.products.attribute import ProductAttributeTypeClass


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
        label=f"test product {now.timestamp()}",
    )


@pytest.fixture
def new_product_family_data() -> dict:
    now = datetime.now()
    return dict(
        name=f"test-family-{now.isoformat()}",
        attribute_ids=[],
        parent_attribute_ids=[],
    )


@pytest.fixture
def new_product_attribute_data() -> dict:
    now = datetime.now()
    return dict(
        name=f"test-attribute-{now.isoformat()}",
        type_class=ProductAttributeTypeClass.TEXT,
        description="Test description",
    )
