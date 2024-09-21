def test_assign_product_to_family(client, new_product_data, new_family_data):
    product = client.products.create_product(**new_product_data)
    family = client.families.create_family(**new_family_data)

    result = client.products.assign_family_to_product(product.id, family.id)

    assert result is True
    assert (client.products.get_product(product.id)).product_family_id == family.id


def test_assign_product_to_family_not_found(client, new_product_data):
    product = client.products.create_product(**new_product_data)

    result = client.products.assign_family_to_product(product.id, "non-existing-id")

    assert result is None


def test_assign_product_to_family_product_not_found(client, new_family_data):
    family = client.families.create_family(**new_family_data)

    result = client.products.assign_family_to_product("non-existing-id", family.id)

    assert result is None


def test_assign_multiple_products_to_family(client, new_product_data, new_family_data):
    product1 = new_product_data.copy()
    product2 = new_product_data.copy()

    product1["sku"] = f"{product1['sku']}-1"
    product2["sku"] = f"{product2['sku']}-2"

    product1 = client.products.create_product(**product1)
    product2 = client.products.create_product(**product2)
    family = client.families.create_family(**new_family_data)

    results = client.products.assign_family_to_products([(product1.id, family.id), (product2.id, family.id)])

    assert results[0] is True
    assert results[1] is True
    assert (client.products.get_product(product1.id)).product_family_id == family.id
    assert (client.products.get_product(product2.id)).product_family_id == family.id
