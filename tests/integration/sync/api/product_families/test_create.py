def test_create_family_ok(client, new_family_data):
    family = client.families.create_family(**new_family_data)

    assert family.name == new_family_data["name"]
    assert family.total_attributes == 0
    assert family.total_models == 0
    assert family.total_products == 0
