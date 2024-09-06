async def test_create_product_ok(client, new_product):
    result = await client.products.create_product(new_product)

    assert result.sku == new_product.sku
    assert result.label == new_product.label
