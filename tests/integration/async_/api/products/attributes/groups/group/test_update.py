async def test_update_attributes_group(plytix, new_product_attributes_group_data):
    group = await plytix.products.attributes.groups.create_attributes_group(**new_product_attributes_group_data)

    updated_attribute = await plytix.products.attributes.groups.update_attributes_group(
        group.id,
        name=f"Updated {group.name}",
    )

    assert updated_attribute is not None
    assert updated_attribute.id == group.id
    assert updated_attribute.name == f"Updated {group.name}"


async def test_update_not_existing_attribute(plytix):
    updated_group = await plytix.products.attributes.groups.update_attributes_group(
        "not-existing-attribute-id",
        name="Updated Name",
    )

    assert updated_group is None


async def test_update_attributes_groups(plytix, new_product_attributes_group_data):
    group1 = new_product_attributes_group_data.copy()
    group2 = new_product_attributes_group_data.copy()

    group1["name"] = f"{group1['name']} 1"
    group2["name"] = f"{group2['name']} 2"

    group1 = await plytix.products.attributes.groups.create_attributes_group(**group1)
    group2 = await plytix.products.attributes.groups.create_attributes_group(**group2)
    assert group1.id is not None
    assert group2.id is not None

    updated_attributes = await plytix.products.attributes.groups.update_attributes_groups(
        [
            {"attributes_group_id": group1.id, "name": f"Updated {group1.name}"},
            {"attributes_group_id": group2.id, "name": f"Updated {group2.name}"},
        ]
    )

    assert len(updated_attributes) == 2
    assert all(updated_attributes)
    assert updated_attributes[0].id == group1.id
    assert updated_attributes[0].name == f"Updated {group1.name}"
    assert updated_attributes[1].id == group2.id
    assert updated_attributes[1].name == f"Updated {group2.name}"
