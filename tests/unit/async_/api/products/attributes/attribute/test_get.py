from http import HTTPStatus, HTTPMethod


async def test_get_attribute(plytix_factory, response_factory, assert_requests_factory, product_attribute):
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                {
                    "id": product_attribute.id,
                    "name": product_attribute.name,
                    "type_class": product_attribute.type_class,
                },
            ),
        ]
    )

    retrieved_product_attribute = await plytix.products.attributes.get_attribute(product_attribute.id)

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.GET,
                path=f"/api/v1/attributes/product/{product_attribute.id}",
            ),
        ]
    )
    assert product_attribute.id == retrieved_product_attribute.id
    assert product_attribute.name == retrieved_product_attribute.name
    assert product_attribute.type_class == retrieved_product_attribute.type_class


async def test_get_attribute_that_does_not_exist(plytix_factory, response_factory):
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.NOT_FOUND),
        ]
    )

    product_attribute = await plytix.products.attributes.get_attribute("non_existent_id")
    assert product_attribute is None


async def test_get_attributes(
    plytix_factory, new_product_attribute_data, response_factory, product_attribute, assert_requests_factory
):
    attribute1 = new_product_attribute_data.copy()
    attribute2 = new_product_attribute_data.copy()
    attribute3 = new_product_attribute_data.copy()

    attribute1["name"] = f"{attribute1['name']}-1"
    attribute2["name"] = f"{attribute2['name']}-2"
    attribute3["name"] = f"{attribute3['name']}-3"

    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                {
                    "id": "1",
                    "name": attribute1["name"],
                    "type_class": attribute1["type_class"],
                },
            ),
            response_factory(
                HTTPStatus.OK,
                {
                    "id": "2",
                    "name": attribute2["name"],
                    "type_class": attribute2["type_class"],
                },
            ),
            response_factory(
                HTTPStatus.OK,
                {
                    "id": "3",
                    "name": attribute3["name"],
                    "type_class": attribute3["type_class"],
                },
            ),
        ]
    )

    retrieved_product_attributes = await plytix.products.attributes.get_attributes(["1", "2", "3"])

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.GET,
                path=f"/api/v1/attributes/product/1",
            ),
            dict(
                method=HTTPMethod.GET,
                path=f"/api/v1/attributes/product/2",
            ),
            dict(
                method=HTTPMethod.GET,
                path=f"/api/v1/attributes/product/3",
            ),
        ]
    )
    assert "1" == retrieved_product_attributes[0].id
    assert attribute1["name"] == retrieved_product_attributes[0].name
    assert attribute1["type_class"] == retrieved_product_attributes[0].type_class

    assert "2" == retrieved_product_attributes[1].id
    assert attribute2["name"] == retrieved_product_attributes[1].name
    assert attribute2["type_class"] == retrieved_product_attributes[1].type_class

    assert "3" == retrieved_product_attributes[2].id
    assert attribute3["name"] == retrieved_product_attributes[2].name
    assert attribute3["type_class"] == retrieved_product_attributes[2].type_class
