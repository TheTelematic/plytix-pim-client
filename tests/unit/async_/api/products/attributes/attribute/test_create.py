from http import HTTPMethod, HTTPStatus


async def test_create_product_attribute(
    plytix_factory, new_product_attribute_data, response_factory, assert_requests_factory
):
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                [
                    {
                        "name": new_product_attribute_data["name"],
                        "type_class": new_product_attribute_data["type_class"],
                        "label": new_product_attribute_data["name"]
                        .lower()
                        .replace(" ", "_")
                        .replace("-", "_")
                        .replace(".", "_")
                        .replace(":", "_"),
                        "groups": [],
                        "id": 1,
                    },
                ],
            ),
        ]
    )

    product_attribute = await plytix.products.attributes.create_attribute(**new_product_attribute_data)

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.POST,
                path="/api/v1/attributes/product",
                json={
                    "name": new_product_attribute_data["name"],
                    "type_class": new_product_attribute_data["type_class"],
                    "description": new_product_attribute_data["description"],
                },
            ),
        ]
    )
    assert product_attribute.name == new_product_attribute_data["name"]
    assert product_attribute.type_class == new_product_attribute_data["type_class"]
    assert product_attribute.label == new_product_attribute_data["name"].lower().replace(" ", "_").replace(
        "-", "_"
    ).replace(".", "_").replace(":", "_")
    assert product_attribute.groups == []
    assert product_attribute.id


async def test_create_multiple_product_attributes(
    plytix_factory, new_product_attribute_data, response_factory, assert_requests_factory
):
    new_product_attribute_data1 = new_product_attribute_data.copy()
    new_product_attribute_data2 = new_product_attribute_data.copy()
    new_product_attribute_data1["name"] = f"{new_product_attribute_data1['name']}-1"
    new_product_attribute_data2["name"] = f"{new_product_attribute_data2['name']}-2"

    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                [
                    {
                        "name": new_product_attribute_data1["name"],
                        "type_class": new_product_attribute_data1["type_class"],
                        "label": new_product_attribute_data1["name"]
                        .lower()
                        .replace(" ", "_")
                        .replace("-", "_")
                        .replace(".", "_")
                        .replace(":", "_"),
                        "groups": [],
                        "id": 1,
                    },
                ],
            ),
            response_factory(
                HTTPStatus.OK,
                [
                    {
                        "name": new_product_attribute_data2["name"],
                        "type_class": new_product_attribute_data2["type_class"],
                        "label": new_product_attribute_data2["name"]
                        .lower()
                        .replace(" ", "_")
                        .replace("-", "_")
                        .replace(".", "_")
                        .replace(":", "_"),
                        "groups": [],
                        "id": 2,
                    },
                ],
            ),
        ]
    )

    product_attributes = await plytix.products.attributes.create_attributes(
        [new_product_attribute_data1, new_product_attribute_data2]
    )

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.POST,
                path="/api/v1/attributes/product",
                json={
                    "name": new_product_attribute_data1["name"],
                    "type_class": new_product_attribute_data1["type_class"],
                    "description": new_product_attribute_data1["description"],
                },
            ),
            dict(
                method=HTTPMethod.POST,
                path="/api/v1/attributes/product",
                json={
                    "name": new_product_attribute_data2["name"],
                    "type_class": new_product_attribute_data2["type_class"],
                    "description": new_product_attribute_data2["description"],
                },
            ),
        ]
    )
    assert len(product_attributes) == 2

    assert product_attributes[0].name == new_product_attribute_data1["name"]
    assert product_attributes[0].type_class == new_product_attribute_data1["type_class"]
    assert product_attributes[0].label == new_product_attribute_data1["name"].lower().replace(" ", "_").replace(
        "-", "_"
    ).replace(".", "_").replace(":", "_")
    assert product_attributes[0].groups == []
    assert product_attributes[0].id

    assert product_attributes[1].name == new_product_attribute_data2["name"]
    assert product_attributes[1].type_class == new_product_attribute_data2["type_class"]
    assert product_attributes[1].label == new_product_attribute_data2["name"].lower().replace(" ", "_").replace(
        "-", "_"
    ).replace(".", "_").replace(":", "_")
    assert product_attributes[1].groups == []
    assert product_attributes[1].id

    assert product_attributes[0].id != product_attributes[1].id
