async def test_delete_product(plytix, new_product_data):
    result = await plytix.products.create_product(new_product_data["sku"], new_product_data["label"])

    result = await plytix.products.delete_product(result.id)

    assert result is True


async def test_delete_product_not_found(plytix):
    result = await plytix.products.delete_product("non-existing-id")

    assert result is False


async def test_delete_multiple_products(plytix, new_product_data):
    new_product_data_1 = new_product_data.copy()
    new_product_data_2 = new_product_data.copy()
    new_product_data_3 = new_product_data.copy()

    new_product_data_1["sku"] = f"{new_product_data['sku']}-1"
    new_product_data_2["sku"] = f"{new_product_data['sku']}-2"
    new_product_data_3["sku"] = f"{new_product_data['sku']}-3"

    products = [
        new_product_data_1,
        new_product_data_2,
        new_product_data_3,
    ]
    results = await plytix.products.create_products(products)

    product_ids = [result.id for result in results]
    results = await plytix.products.delete_products(product_ids)

    assert results[0] is True
    assert results[1] is True
    assert results[2] is True
