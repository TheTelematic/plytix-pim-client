def test_rename_family(plytix, new_product_family_data):
    result = plytix.products.families.create_family(**new_product_family_data)

    new_name = f"{new_product_family_data['name']}-new"
    result = plytix.products.families.rename_family(result.id, new_name)

    assert result.name == new_name


def test_rename_family_not_found(plytix):
    result = plytix.products.families.rename_family("non-existing-id", "new name")

    assert result is None


def test_update_multiple_families(plytix, new_product_family_data):
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
    results = plytix.products.families.create_families(families)

    updated_families = [(result.id, f"{result.name}-new") for result in results]
    results = plytix.products.families.rename_families(updated_families)

    assert results[0].name == f"{new_family_data_1['name']}-new"
    assert results[1].name == f"{new_family_data_2['name']}-new"
    assert results[2].name == f"{new_family_data_3['name']}-new"
