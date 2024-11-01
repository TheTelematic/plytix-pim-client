async def test_create_product_relationship(plytix_factory, new_product_relationship_data):
    product_relationship = await plytix_factory.products.relationships.create_product_relationship(
        **new_product_relationship_data
    )
    assert product_relationship.name == new_product_relationship_data["name"]


async def test_create_product_relationships(plytix_factory, new_product_relationship_data):
    relationship1 = new_product_relationship_data.copy()
    relationship2 = new_product_relationship_data.copy()

    relationship1["name"] = f"{relationship1['name']}-1"
    relationship2["name"] = f"{relationship2['name']}-2"

    product_relationships = await plytix_factory.products.relationships.create_product_relationships(
        [relationship1, relationship2]
    )
    assert product_relationships[0].name == relationship1["name"]
    assert product_relationships[1].name == relationship2["name"]
