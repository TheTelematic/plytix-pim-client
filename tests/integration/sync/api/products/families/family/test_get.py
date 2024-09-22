def test_get_family(client, new_product_family_data):
    result = client.products.families.create_family(**new_product_family_data)

    result = client.products.families.get_family(result.id)

    assert result.name == new_product_family_data["name"]


def test_get_family_not_found(client):
    result = client.products.families.get_family("non-existing-id")

    assert result is None


def test_get_multiple_families(client, new_product_family_data):
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
    results = client.products.families.create_families(families)

    family_ids = [result.id for result in results]
    results = client.products.families.get_families(family_ids)

    assert len(results) == 3
    assert results[0].name == new_family_data_1["name"]
    assert results[1].name == new_family_data_2["name"]
    assert results[2].name == new_family_data_3["name"]
