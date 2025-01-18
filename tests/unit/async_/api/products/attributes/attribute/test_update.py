from http import HTTPStatus, HTTPMethod


async def test_update_attribute(
    plytix_factory,
    product_attribute,
    response_factory,
    assert_requests_factory,
):
    new_name = f"Updated {product_attribute.name}"
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                {
                    "id": product_attribute.id,
                    "name": new_name,
                    "type_class": product_attribute.type_class,
                },
            ),
        ]
    )

    updated_attribute = await plytix.products.attributes.update_attribute(
        product_attribute.id,
        new_name=new_name,
    )

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.PATCH,
                path=f"/api/v1/attributes/product/{product_attribute.id}",
                json={"name": new_name},
            ),
        ]
    )
    assert updated_attribute is not None
    assert updated_attribute.id == product_attribute.id
    assert updated_attribute.name == new_name


async def test_update_not_existing_attribute(plytix_factory, response_factory):
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.NOT_FOUND),
        ]
    )

    updated_attribute = await plytix.products.attributes.update_attribute(
        "not-existing-attribute-id",
        new_name="Updated Name",
    )

    assert updated_attribute is None


async def test_update_attributes(plytix_factory, new_product_attribute_data, response_factory):
    attribute1 = new_product_attribute_data.copy()
    attribute2 = new_product_attribute_data.copy()

    attribute1["name"] = f"{attribute1['name']} 1"
    attribute2["name"] = f"{attribute2['name']} 2"

    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                {
                    "id": "1",
                    "name": f"Updated {attribute1["name"]}",
                    "type_class": attribute1["type_class"],
                },
            ),
            response_factory(
                HTTPStatus.OK,
                {
                    "id": "2",
                    "name": f"Updated {attribute2["name"]}",
                    "type_class": attribute2["type_class"],
                },
            ),
        ]
    )

    updated_attributes = await plytix.products.attributes.update_attributes(
        [
            ("1", f"Updated {attribute1["name"]}"),
            ("2", f"Updated {attribute2["name"]}"),
        ]
    )

    assert len(updated_attributes) == 2
    assert all(updated_attributes)
    assert updated_attributes[0].id == "1"
    assert updated_attributes[0].name == f"Updated {attribute1["name"]}"
    assert updated_attributes[1].id == "2"
    assert updated_attributes[1].name == f"Updated {attribute2["name"]}"
