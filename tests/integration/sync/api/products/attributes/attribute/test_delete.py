def test_delete_attribute(plytix, new_product_attribute_data):
    product_attribute = plytix.products.attributes.create_attribute(**new_product_attribute_data)
    assert product_attribute.id

    deleted = plytix.products.attributes.delete_attribute(product_attribute.id)
    assert deleted

    product_attribute = plytix.products.attributes.get_attribute(product_attribute.id)
    assert product_attribute is None


def test_delete_attribute_that_does_not_exist(plytix):
    deleted = plytix.products.attributes.delete_attribute("non_existent_id")
    assert not deleted


def test_delete_attributes(plytix, new_product_attribute_data):
    attribute1 = new_product_attribute_data.copy()
    attribute2 = new_product_attribute_data.copy()
    attribute3 = new_product_attribute_data.copy()

    attribute1["name"] = f"{attribute1['name']}-1"
    attribute2["name"] = f"{attribute2['name']}-2"
    attribute3["name"] = f"{attribute3['name']}-3"

    product_attributes = [
        plytix.products.attributes.create_attribute(**attribute1),
        plytix.products.attributes.create_attribute(**attribute2),
        plytix.products.attributes.create_attribute(**attribute3),
    ]
    assert all(product_attribute.id for product_attribute in product_attributes)

    deleted = plytix.products.attributes.delete_attributes(
        [product_attribute.id for product_attribute in product_attributes]
    )
    assert all(deleted)

    product_attributes = plytix.products.attributes.get_attributes(
        [product_attribute.id for product_attribute in product_attributes]
    )
    assert all(product_attribute is None for product_attribute in product_attributes)
