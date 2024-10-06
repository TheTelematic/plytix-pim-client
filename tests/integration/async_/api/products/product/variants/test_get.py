async def test_get_products_variants(plytix, product, product_variant):
    result = await plytix.products.variants.get_product_variants(product.id)

    assert len(result) == 1
    assert result[0].id == product_variant.id


async def test_get_products_variants_empty(plytix, product):
    result = await plytix.products.variants.get_product_variants(product.id)

    assert result == []


async def test_get_multiple_products_variants(plytix, product, product_variant):
    result = await plytix.products.variants.get_multiple_product_variants([product.id])

    assert len(result) == 1
    assert len(result[0]) == 1
    assert result[0][0].id == product_variant.id


async def test_get_multiple_products_variants_empty(plytix, product):
    result = await plytix.products.variants.get_multiple_product_variants([product.id])

    assert result == [[]]


async def test_get_products_variants_not_found(plytix):
    result = await plytix.products.variants.get_product_variants("not_found")

    assert result is None


async def test_get_multiple_products_variants_not_found(plytix):
    result = await plytix.products.variants.get_multiple_product_variants(["not_found"])

    assert result == [None]
