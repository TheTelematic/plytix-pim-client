def test_update_product(plytix, new_product_data):
    result = plytix.products.create_product(new_product_data["sku"], new_product_data["label"])

    new_label = "new label"
    result = plytix.products.update_product(result.id, {"label": new_label})

    assert result.sku == new_product_data["sku"]
    assert result.label == new_label


def test_update_product_not_found(plytix):
    result = plytix.products.update_product("non-existing-id", {"label": "new label"})

    assert result is None


def test_update_multiple_products(plytix, new_product_data):
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
    results = plytix.products.create_products(products)

    new_label = "new label"
    updated_products = [(result.id, {"label": new_label}) for result in results]
    results = plytix.products.update_products(updated_products)

    assert results[0].sku == new_product_data_1["sku"]
    assert results[0].label == new_label

    assert results[1].sku == new_product_data_2["sku"]
    assert results[1].label == new_label

    assert results[2].sku == new_product_data_3["sku"]
    assert results[2].label == new_label
