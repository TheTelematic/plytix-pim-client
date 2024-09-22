async def test_get_family(plytix, new_product_family_data):
    result = await plytix.products.families.create_family(**new_product_family_data)

    result = await plytix.products.families.get_family(result.id)

    assert result.name == new_product_family_data["name"]


async def test_get_family_not_found(plytix):
    result = await plytix.products.families.get_family("non-existing-id")

    assert result is None


async def test_get_multiple_families(plytix, new_product_family_data):
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
    results = await plytix.products.families.create_families(families)

    family_ids = [result.id for result in results]
    results = await plytix.products.families.get_families(family_ids)

    assert len(results) == 3
    assert results[0].name == new_family_data_1["name"]
    assert results[1].name == new_family_data_2["name"]
    assert results[2].name == new_family_data_3["name"]
