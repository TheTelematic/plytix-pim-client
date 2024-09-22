async def test_get_product(plytix, new_product_data):
    result = await plytix.products.create_product(new_product_data["sku"], new_product_data["label"])

    result = await plytix.products.get_product(result.id)

    assert result.sku == new_product_data["sku"]
    assert result.label == new_product_data["label"]


async def test_get_product_not_found(plytix):
    result = await plytix.products.get_product("non-existing-id")

    assert result is None


async def test_get_multiple_products(plytix, new_product_data):
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
    results = await plytix.products.get_products(product_ids)

    assert results[0].sku == new_product_data_1["sku"]
    assert results[0].label == new_product_data_1["label"]

    assert results[1].sku == new_product_data_2["sku"]
    assert results[1].label == new_product_data_2["label"]

    assert results[2].sku == new_product_data_3["sku"]
    assert results[2].label == new_product_data_3["label"]
