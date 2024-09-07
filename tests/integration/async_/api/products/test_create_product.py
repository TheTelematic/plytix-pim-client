async def test_create_product_ok(client, new_product_data):
    result = await client.products.create_product(new_product_data["sku"], new_product_data["label"])

    assert result.sku == new_product_data["sku"]
    assert result.label == new_product_data["label"]
