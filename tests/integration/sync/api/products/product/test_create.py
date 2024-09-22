def test_create_product_ok(plytix, new_product_data):
    result = plytix.products.create_product(new_product_data["sku"], new_product_data["label"])

    assert result.sku == new_product_data["sku"]
    assert result.label == new_product_data["label"]


def test_create_product_no_label(plytix, new_product_data):
    result = plytix.products.create_product(new_product_data["sku"])

    assert result.sku == new_product_data["sku"]
    assert result.label is None


def test_create_multiple_products(plytix, new_product_data):
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

    assert results[0].sku == new_product_data_1["sku"]
    assert results[0].label == new_product_data_1["label"]

    assert results[1].sku == new_product_data_2["sku"]
    assert results[1].label == new_product_data_2["label"]

    assert results[2].sku == new_product_data_3["sku"]
    assert results[2].label == new_product_data_3["label"]
