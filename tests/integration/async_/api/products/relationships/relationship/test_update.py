async def test_update_relationship(plytix, new_product_relationship_data):
    relationship = await plytix.products.relationships.create_product_relationship(**new_product_relationship_data)

    updated_relationship = await plytix.products.relationships.update_relationship(
        relationship.id,
        new_name=f"Updated {relationship.name}",
    )

    assert updated_relationship is not None
    assert updated_relationship.id == relationship.id
    assert updated_relationship.name == f"Updated {relationship.name}"


async def test_update_not_existing_relationship(plytix):
    updated_relationship = await plytix.products.relationships.update_relationship(
        "not-existing-relationship-id",
        new_name="Updated Name",
    )

    assert updated_relationship is None


async def test_update_relationships(plytix, new_product_relationship_data):
    relationship1 = new_product_relationship_data.copy()
    relationship2 = new_product_relationship_data.copy()

    relationship1["name"] = f"{relationship1['name']} 1"
    relationship2["name"] = f"{relationship2['name']} 2"

    relationship1 = await plytix.products.relationships.create_product_relationship(**relationship1)
    relationship2 = await plytix.products.relationships.create_product_relationship(**relationship2)

    updated_relationships = await plytix.products.relationships.update_relationships(
        [
            (relationship1.id, f"Updated {relationship1.name}"),
            (relationship2.id, f"Updated {relationship2.name}"),
        ]
    )

    assert len(updated_relationships) == 2
    assert all(updated_relationships)
    assert updated_relationships[0].id == relationship1.id
    assert updated_relationships[0].name == f"Updated {relationship1.name}"
    assert updated_relationships[1].id == relationship2.id
    assert updated_relationships[1].name == f"Updated {relationship2.name}"
