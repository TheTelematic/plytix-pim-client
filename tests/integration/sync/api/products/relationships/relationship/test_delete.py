def test_delete_product_relationship(plytix, new_product_relationship_data):
    product_relationship = plytix.products.relationships.create_product_relationship(**new_product_relationship_data)

    result = plytix.products.relationships.delete_product_relationship(product_relationship.id)

    assert result is True


def test_delete_product_relationship_with_non_existent_relationship(plytix):
    result = plytix.products.relationships.delete_product_relationship("non-existent-id")

    assert result is False


def test_delete_product_relationships(plytix, new_product_relationship_data):
    relationship1 = new_product_relationship_data.copy()
    relationship2 = new_product_relationship_data.copy()
    relationship1["name"] = f"{relationship1['name']} 1"
    relationship2["name"] = f"{relationship2['name']} 2"
    relationship1 = plytix.products.relationships.create_product_relationship(**relationship1)
    relationship2 = plytix.products.relationships.create_product_relationship(**relationship2)

    result = plytix.products.relationships.delete_product_relationships([relationship1.id, relationship2.id])

    assert result == [True, True]
