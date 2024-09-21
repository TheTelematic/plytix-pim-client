async def test_create_family_ok(client, new_family_data):
    family = await client.families.create_family(**new_family_data)

    assert family.name == new_family_data["name"]
    assert family.total_attributes == 0
    assert family.total_models == 0
    assert family.total_products == 0


async def test_create_family_multiple_ok(client, new_family_data):
    family1 = new_family_data.copy()
    family2 = new_family_data.copy()
    family1["name"] = f"{family1['name']}-1"
    family2["name"] = f"{family2['name']}-2"

    families = await client.families.create_families([family1, family2])

    assert len(families) == 2
    assert families[0].name == family1["name"]
    assert families[1].name == family2["name"]
    assert families[0].total_attributes == 0
    assert families[1].total_attributes == 0
    assert families[0].total_models == 0
    assert families[1].total_models == 0
    assert families[0].total_products == 0
    assert families[1].total_products == 0
