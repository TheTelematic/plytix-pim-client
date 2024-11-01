async def test_get_attribute(plytix_factory, new_product_attribute_data):
    product_attribute = await plytix_factory.products.attributes.create_attribute(**new_product_attribute_data)

    retrieved_product_attribute = await plytix_factory.products.attributes.get_attribute(product_attribute.id)

    assert product_attribute.id == retrieved_product_attribute.id
    assert product_attribute.name == retrieved_product_attribute.name
    assert product_attribute.type_class == retrieved_product_attribute.type_class


async def test_get_attribute_that_does_not_exist(plytix_factory):
    product_attribute = await plytix_factory.products.attributes.get_attribute("non_existent_id")
    assert product_attribute is None


async def test_get_attributes(plytix_factory, new_product_attribute_data):
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

    retrieved_product_attributes = await plytix_factory.products.attributes.get_attributes(
        [product_attribute.id for product_attribute in product_attributes]
    )

    assert product_attributes[0].id == retrieved_product_attributes[0].id
    assert product_attributes[1].id == retrieved_product_attributes[1].id
    assert product_attributes[2].id == retrieved_product_attributes[2].id
    assert product_attributes[0].name == retrieved_product_attributes[0].name
    assert product_attributes[1].name == retrieved_product_attributes[1].name
    assert product_attributes[2].name == retrieved_product_attributes[2].name
    assert product_attributes[0].type_class == retrieved_product_attributes[0].type_class
    assert product_attributes[1].type_class == retrieved_product_attributes[1].type_class
    assert product_attributes[2].type_class == retrieved_product_attributes[2].type_class