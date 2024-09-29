import asyncio
import shutil
from datetime import datetime
from pathlib import Path
from typing import Callable

import httpx
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


@pytest.fixture
def new_asset_data_from_url_factory() -> Callable[[], dict]:
    def factory() -> dict:
        with httpx.Client() as client:
            response = client.get("https://picsum.photos/200/300")
            return dict(
                url=response.headers["Location"],
                filename=f"test-{str(datetime.now().timestamp()).replace('.', '')}.jpg",
            )

    return factory


@pytest.fixture
def new_asset_data_from_local_file_factory() -> Callable[[], dict]:
    def factory() -> dict:
        destination_file = f"/tmp/test-{str(datetime.now().timestamp()).replace('.', '')}.py"
        shutil.copy(Path(Path(__file__).parent.resolve(), "resources", "assets", "Plytix.jpeg"), destination_file)

        return dict(file_path=destination_file)

    return factory


@pytest.fixture
def new_asset_category_data() -> dict:
    now = datetime.now()
    return dict(name=f"test-category-{now.isoformat()}")


@pytest.fixture
def new_product_category_data() -> dict:
    now = datetime.now()
    return dict(name=f"test-category-{now.isoformat()}")
