async def test_update_quantity_product_relationship(plytix_factory, product, product_relationship, product_related):
    result = await plytix_factory.products.relationships.update_quantity_product_relationship(
        product.id,
        product_relationship.id,
        product_related.id,
        10,
    )

    assert result is not None
    product = await plytix_factory.products.get_product(product.id)
    assert product.relationships[0]["related_products"][0]["quantity"] == 10


async def test_update_quantity_product_relationship_not_found(plytix_factory):
    result = await plytix_factory.products.relationships.update_quantity_product_relationship(
        "not-found",
        "not-found",
        "not-found",
        10,
    )

    assert result is None


async def test_update_quantity_multiple_product_relationships(plytix_factory, product, product_relationship, product_related):
    assert product.id is not None
    assert product_relationship.id is not None
    assert product_related.id is not None

    results = await plytix_factory.products.relationships.update_quantity_multiple_product_relationships(
        [
            {
                "product_id": product.id,
                "product_relationship_id": product_relationship.id,
                "related_product_id": product_related.id,
                "quantity": 10,
            }
        ]
    )

    assert len(results) == 1
    assert results[0] is not None
    product = await plytix_factory.products.get_product(product.id)
    assert product.relationships[0]["related_products"][0]["quantity"] == 10