from http import HTTPStatus, HTTPMethod


async def test_delete_attribute(plytix_factory, response_factory, assert_requests_factory):
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.NO_CONTENT,
            ),
        ]
    )
    product_attribute_id = "1234"

    deleted = await plytix.products.attributes.delete_attribute(product_attribute_id)

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.DELETE,
                path=f"/api/v1/attributes/product/{product_attribute_id}",
            ),
        ]
    )
    assert deleted


async def test_delete_attribute_that_does_not_exist(plytix_factory, response_factory, assert_requests_factory):
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.NOT_FOUND,
            ),
        ]
    )
    product_attribute_id = "1234"

    deleted = await plytix.products.attributes.delete_attribute(product_attribute_id)

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.DELETE,
                path=f"/api/v1/attributes/product/{product_attribute_id}",
            ),
        ]
    )
    assert not deleted


async def test_delete_attributes(plytix_factory, new_product_attribute_data):
    attribute1 = new_product_attribute_data.copy()
    attribute2 = new_product_attribute_data.copy()
    attribute3 = new_product_attribute_data.copy()

    attribute1["name"] = f"{attribute1['name']}-1"
    attribute2["name"] = f"{attribute2['name']}-2"
    attribute3["name"] = f"{attribute3['name']}-3"

    product_attributes = [
        await plytix_factory.products.attributes.create_attribute(**attribute1),
        await plytix_factory.products.attributes.create_attribute(**attribute2),
        await plytix_factory.products.attributes.create_attribute(**attribute3),
    ]
    assert all(product_attribute.id for product_attribute in product_attributes)

    deleted = await plytix_factory.products.attributes.delete_attributes(
        [product_attribute.id for product_attribute in product_attributes]
    )
    assert all(deleted)

    product_attributes = await plytix_factory.products.attributes.get_attributes(
        [product_attribute.id for product_attribute in product_attributes]
    )
    assert all(product_attribute is None for product_attribute in product_attributes)
