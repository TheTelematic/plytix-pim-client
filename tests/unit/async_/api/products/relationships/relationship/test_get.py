async def test_get_relationship(plytix_factory, new_product_relationship_data):
    product_relationship = await plytix_factory.products.relationships.create_product_relationship(
        **new_product_relationship_data
    )

    retrieved_product_relationship = await plytix_factory.products.relationships.get_relationship(product_relationship.id)

    assert product_relationship.id == retrieved_product_relationship.id
    assert product_relationship.name == retrieved_product_relationship.name
    assert product_relationship.label == retrieved_product_relationship.label


async def test_get_relationship_that_does_not_exist(plytix_factory):
    product_relationship = await plytix_factory.products.relationships.get_relationship("non_existent_id")
    assert product_relationship is None


async def test_get_relationships(plytix_factory, new_product_relationship_data):
    relationship1 = new_product_relationship_data.copy()
    relationship2 = new_product_relationship_data.copy()
    relationship3 = new_product_relationship_data.copy()

    relationship1["name"] = f"{relationship1['name']}-1"
    relationship2["name"] = f"{relationship2['name']}-2"
    relationship3["name"] = f"{relationship3['name']}-3"

    product_relationships = [
        await plytix_factory.products.relationships.create_product_relationship(**relationship1),
        await plytix_factory.products.relationships.create_product_relationship(**relationship2),
        await plytix_factory.products.relationships.create_product_relationship(**relationship3),
    ]

    retrieved_product_relationships = await plytix_factory.products.relationships.get_relationships(
        [product_relationship.id for product_relationship in product_relationships]
    )

    assert product_relationships[0].id == retrieved_product_relationships[0].id
    assert product_relationships[1].id == retrieved_product_relationships[1].id
    assert product_relationships[2].id == retrieved_product_relationships[2].id
    assert product_relationships[0].name == retrieved_product_relationships[0].name
    assert product_relationships[1].name == retrieved_product_relationships[1].name
    assert product_relationships[2].name == retrieved_product_relationships[2].name
    assert product_relationships[0].label == retrieved_product_relationships[0].label
    assert product_relationships[1].label == retrieved_product_relationships[1].label
    assert product_relationships[2].label == retrieved_product_relationships[2].label
