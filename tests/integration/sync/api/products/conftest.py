from datetime import datetime

import pytest

from plytix_pim_client.dtos.product import Product


@pytest.fixture
def new_product() -> Product:
    now = datetime.now()
    return Product(
        sku=f"test-product-{now.isoformat()}",
        label=f"test_product_{str(now.timestamp()).replace('.', '')}",
    )
