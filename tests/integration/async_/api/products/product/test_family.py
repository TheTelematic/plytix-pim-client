async def test_assign_product_to_family(client, new_product_data, new_product_family_data):
    product = await client.products.create_product(**new_product_data)
    family = await client.products.families.create_family(**new_product_family_data)

    result = await client.products.assign_family(product.id, family.id)

    assert result is True
    assert (await client.products.get_product(product.id)).product_family_id == family.id


async def test_assign_product_to_family_not_found(client, new_product_data):
    product = await client.products.create_product(**new_product_data)

    result = await client.products.assign_family(product.id, "non-existing-id")

    assert result is None


async def test_assign_product_to_family_product_not_found(client, new_product_family_data):
    family = await client.products.families.create_family(**new_product_family_data)

    result = await client.products.assign_family("non-existing-id", family.id)

    assert result is None


async def test_assign_multiple_products_to_family(client, new_product_data, new_product_family_data):
    product1 = new_product_data.copy()
    product2 = new_product_data.copy()

    product1["sku"] = f"{product1['sku']}-1"
    product2["sku"] = f"{product2['sku']}-2"

    product1 = await client.products.create_product(**product1)
    product2 = await client.products.create_product(**product2)
    family = await client.products.families.create_family(**new_product_family_data)

    results = await client.products.assign_families([(product1.id, family.id), (product2.id, family.id)])

    assert results[0] is True
    assert results[1] is True
    assert (await client.products.get_product(product1.id)).product_family_id == family.id
    assert (await client.products.get_product(product2.id)).product_family_id == family.id
