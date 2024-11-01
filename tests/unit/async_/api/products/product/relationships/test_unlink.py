import pytest


@pytest.mark.skip("To be fixed in https://github.com/TheTelematic/plytix-pim-client/issues/44")
async def test_unlink_relationship_to_product(plytix_factory, product, product_relationship, new_product_data):
    product2 = new_product_data.copy()
    product2["sku"] = f"{product2['sku']}-2"
    product2 = await plytix_factory.products.create_product(**product2)
    assert product2.id is not None
    await plytix_factory.products.relationships.link_product_to_relationship(
        product.id, product_relationship.id, [{"product_id": product2.id, "quantity": 1}]
    )

    result = await plytix_factory.products.relationships.unlink_product_from_relationship(
        product.id, product_relationship.id, [product2.id]
    )

    assert result is True
    product = await plytix_factory.products.get_product(product.id)
    assert product.relationships == []


@pytest.mark.skip("To be fixed in https://github.com/TheTelematic/plytix-pim-client/issues/44")
async def test_unlink_not_existing_product(plytix_factory):
    result = await plytix_factory.products.relationships.unlink_product_from_relationship(
        "not-existing", "not-existing", ["not-existing"]
    )

    assert result is False


@pytest.mark.skip("To be fixed in https://github.com/TheTelematic/plytix-pim-client/issues/44")
async def test_multiple_products_to_relationships(
        plytix_factory, product, product_relationship, new_product_data, new_product_relationship_data
):
    assert product.id is not None
    assert product_relationship.id is not None
    product2 = new_product_data.copy()
    product2["sku"] = f"{product2['sku']}-2"
    product2 = await plytix_factory.products.create_product(**product2)
    assert product2.id is not None
    product3 = new_product_data.copy()
    product3["sku"] = f"{product3['sku']}-3"
    product3 = await plytix_factory.products.create_product(**product3)
    assert product3.id is not None
    await plytix_factory.products.relationships.link_product_to_relationships(
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

    results = await plytix_factory.products.relationships.unlink_product_from_relationships(
        [
            {
                "product_id": product.id,
                "product_relationship_id": product_relationship.id,
                "product_ids_to_unlink": [product2.id],
            },
            {
                "product_id": product.id,
                "product_relationship_id": product_relationship.id,
                "product_ids_to_unlink": [product3.id],
            },
        ]
    )

    assert results == [True, True]
    product = await plytix_factory.products.get_product(product.id)
    product2 = await plytix_factory.products.get_product(product2.id)
    assert product.relationships == []
    assert product2.relationships == []
