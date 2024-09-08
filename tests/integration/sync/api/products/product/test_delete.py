def test_delete_product(client, new_product_data):
    result = client.products.create_product(new_product_data["sku"], new_product_data["label"])

    result = client.products.delete_product(result.id)

    assert result is True


def test_delete_product_not_found(client):
    result = client.products.delete_product("non-existing-id")

    assert result is False


def test_delete_multiple_products(client, new_product_data):
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
    results = client.products.create_products(products)

    product_ids = [result.id for result in results]
    results = client.products.delete_products(product_ids)

    assert results[0] is True
    assert results[1] is True
    assert results[2] is True
