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


async def test_delete_attributes(plytix_factory, response_factory, assert_requests_factory):
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.NO_CONTENT,
            ),
            response_factory(
                HTTPStatus.NO_CONTENT,
            ),
            response_factory(
                HTTPStatus.NO_CONTENT,
            ),
        ]
    )
    product_attribute_ids = [
        "1234",
        "5678",
        "9012",
    ]

    deleted = await plytix.products.attributes.delete_attributes(product_attribute_ids)

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.DELETE,
                path=f"/api/v1/attributes/product/1234",
            ),
            dict(
                method=HTTPMethod.DELETE,
                path=f"/api/v1/attributes/product/5678",
            ),
            dict(
                method=HTTPMethod.DELETE,
                path=f"/api/v1/attributes/product/9012",
            ),
        ]
    )
    assert all(deleted)
