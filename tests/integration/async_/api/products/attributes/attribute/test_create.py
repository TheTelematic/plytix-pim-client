async def test_create_product_attribute(client, new_product_attribute_data):
    product_attribute = await client.products.attributes.create_attribute(**new_product_attribute_data)

    assert product_attribute.name == new_product_attribute_data["name"]
    assert product_attribute.type_class == new_product_attribute_data["type_class"]
    assert product_attribute.label == new_product_attribute_data["name"].lower().replace(" ", "_").replace(
        "-", "_"
    ).replace(".", "_").replace(":", "_")
    assert product_attribute.groups == []
    assert product_attribute.id
    assert product_attribute.filter_type == "TextAttribute"


async def test_create_multiple_product_attributes(client, new_product_attribute_data):
    new_product_attribute_data1 = new_product_attribute_data.copy()
    new_product_attribute_data2 = new_product_attribute_data.copy()
    new_product_attribute_data1["name"] = f"{new_product_attribute_data1['name']}-1"
    new_product_attribute_data2["name"] = f"{new_product_attribute_data2['name']}-2"

    product_attributes = await client.products.attributes.create_attributes(
        [new_product_attribute_data1, new_product_attribute_data2]
    )

    assert len(product_attributes) == 2

    assert product_attributes[0].name == new_product_attribute_data1["name"]
    assert product_attributes[0].type_class == new_product_attribute_data1["type_class"]
    assert product_attributes[0].label == new_product_attribute_data1["name"].lower().replace(" ", "_").replace(
        "-", "_"
    ).replace(".", "_").replace(":", "_")
    assert product_attributes[0].groups == []
    assert product_attributes[0].id
    assert product_attributes[0].filter_type == "TextAttribute"

    assert product_attributes[1].name == new_product_attribute_data2["name"]
    assert product_attributes[1].type_class == new_product_attribute_data2["type_class"]
    assert product_attributes[1].label == new_product_attribute_data2["name"].lower().replace(" ", "_").replace(
        "-", "_"
    ).replace(".", "_").replace(":", "_")
    assert product_attributes[1].groups == []
    assert product_attributes[1].id
    assert product_attributes[1].filter_type == "TextAttribute"

    assert product_attributes[0].id != product_attributes[1].id
