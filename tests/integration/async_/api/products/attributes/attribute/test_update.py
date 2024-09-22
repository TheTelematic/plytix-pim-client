async def test_update_attribute(client, new_product_attribute_data):
    attribute = await client.products.attributes.create_attribute(**new_product_attribute_data)

    updated_attribute = await client.products.attributes.update_attribute(
        attribute.id,
        new_name=f"Updated {attribute.name}",
        description=f"Updated {attribute.description}",
    )

    assert updated_attribute is not None
    assert updated_attribute.id == attribute.id
    assert updated_attribute.name == f"Updated {attribute.name}"
    assert updated_attribute.description == f"Updated {attribute.description}"


async def test_update_not_existing_attribute(client):
    updated_attribute = await client.products.attributes.update_attribute(
        "not-existing-attribute-id",
        new_name="Updated Name",
        description="Updated Description",
    )

    assert updated_attribute is None


async def test_update_attributes(client, new_product_attribute_data):
    attribute1 = new_product_attribute_data.copy()
    attribute2 = new_product_attribute_data.copy()

    attribute1["name"] = f"{attribute1['name']} 1"
    attribute2["name"] = f"{attribute2['name']} 2"

    attribute1 = await client.products.attributes.create_attribute(**attribute1)
    attribute2 = await client.products.attributes.create_attribute(**attribute2)

    updated_attributes = await client.products.attributes.update_attributes(
        [
            (attribute1.id, f"Updated {attribute1.name}", f"Updated {attribute1.description}"),
            (attribute2.id, f"Updated {attribute2.name}", f"Updated {attribute2.description}"),
        ]
    )

    assert len(updated_attributes) == 2
    assert all(updated_attributes)
    assert updated_attributes[0].id == attribute1.id
    assert updated_attributes[0].name == f"Updated {attribute1.name}"
    assert updated_attributes[0].description == f"Updated {attribute1.description}"
    assert updated_attributes[1].id == attribute2.id
    assert updated_attributes[1].name == f"Updated {attribute2.name}"
    assert updated_attributes[1].description == f"Updated {attribute2.description}"
