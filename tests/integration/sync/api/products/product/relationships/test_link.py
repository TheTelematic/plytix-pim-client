def test_link_product_to_relationship(plytix, product, product_relationship, new_product_data):
    product2 = new_product_data.copy()
    product2["sku"] = f"{product2['sku']}-2"
    product2 = plytix.products.create_product(**product2)
    assert product2.id is not None

    relationship = plytix.products.relationships.link_product_to_relationship(
        product.id,
        product_relationship.id,
        [{"product_id": product2.id, "quantity": 1}],
    )

    assert relationship is not None
    assert relationship.id == product_relationship.id
    assert relationship.label == product_relationship.label
    assert len(relationship.related_products) == 1
    assert relationship.related_products[0].product_id == product2.id
    assert relationship.related_products[0].quantity == 1
    assert relationship.related_products[0].last_modified is not None


def test_link_product_to_relationships_not_found(plytix):
    relationship = plytix.products.relationships.link_product_to_relationship(
        "not-found",
        "not-found",
        [{"product_id": "not-found", "quantity": 1}],
    )

    assert relationship is None


def test_link_products_to_relationships(plytix, product, product_relationship, new_product_data):
    assert product.id is not None
    assert product_relationship.id is not None
    product2 = new_product_data.copy()
    product2["sku"] = f"{product2['sku']}-2"
    product2 = plytix.products.create_product(**product2)
    assert product2.id is not None
    product3 = new_product_data.copy()
    product3["sku"] = f"{product3['sku']}-3"
    product3 = plytix.products.create_product(**product3)
    assert product3.id is not None

    relationships = plytix.products.relationships.link_product_to_relationships(
        [
            {
                "product_id": product.id,
                "product_relationship_id": product_relationship.id,
                "product_relationships": [
                    {"product_id": product2.id, "quantity": 1},
                    {"product_id": product3.id, "quantity": 2},
                ],
            }
        ]
    )

    assert relationships is not None
    assert len(relationships) == 1
    relationship = relationships[0]
    assert relationship.id == product_relationship.id
    assert relationship.label == product_relationship.label
    assert len(relationship.related_products) == 2
    assert relationship.related_products[0].product_id == product2.id
    assert relationship.related_products[0].quantity == 1
    assert relationship.related_products[0].last_modified is not None
    assert relationship.related_products[1].product_id == product3.id
    assert relationship.related_products[1].quantity == 2
    assert relationship.related_products[1].last_modified is not None
