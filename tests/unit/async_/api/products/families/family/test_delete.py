async def test_delete_family(plytix_factory, new_product_family_data):
    result = await plytix_factory.products.families.create_family(**new_product_family_data)

    result = await plytix_factory.products.families.delete_family(result.id)

    assert result is True


async def test_delete_family_not_found(plytix_factory):
    result = await plytix_factory.products.families.delete_family("non-existing-id")

    assert result is False


async def test_delete_multiple_products(plytix_factory, new_product_family_data):
    new_family_data_1 = new_product_family_data.copy()
    new_family_data_2 = new_product_family_data.copy()
    new_family_data_3 = new_product_family_data.copy()

    new_family_data_1["name"] = f"{new_product_family_data['name']}-1"
    new_family_data_2["name"] = f"{new_product_family_data['name']}-2"
    new_family_data_3["name"] = f"{new_product_family_data['name']}-3"

    families = [
        new_family_data_1,
        new_family_data_2,
        new_family_data_3,
    ]
    results = await plytix_factory.products.families.create_families(families)

    family_ids = [result.id for result in results]
    results = await plytix_factory.products.families.delete_families(family_ids)

    assert results[0] is True
    assert results[1] is True
    assert results[2] is True
