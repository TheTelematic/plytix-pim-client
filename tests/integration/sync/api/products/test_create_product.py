def test_create_product_ok(client, new_product_data):
    result = client.products.create_product(new_product_data["sku"], new_product_data["label"])

    assert result.sku == new_product_data["sku"]
    assert result.label == new_product_data["label"]


def test_create_product_no_label(client, new_product_data):
    result = client.products.create_product(new_product_data["sku"])

    assert result.sku == new_product_data["sku"]
    assert result.label is None
