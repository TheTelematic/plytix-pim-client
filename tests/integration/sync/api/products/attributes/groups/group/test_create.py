def test_create_product_attributes_group(plytix, new_product_attributes_group_data):
    product_attributes_group = plytix.products.attributes.groups.create_attributes_group(
        **new_product_attributes_group_data
    )

    assert product_attributes_group.name == new_product_attributes_group_data["name"]
    assert product_attributes_group.attribute_labels == new_product_attributes_group_data["attribute_labels"]
    assert product_attributes_group.order == new_product_attributes_group_data["order"]


def test_create_multiple_product_attributes_groups(plytix, new_product_attributes_group_data):
    new_product_attributes_group_data1 = new_product_attributes_group_data.copy()
    new_product_attributes_group_data2 = new_product_attributes_group_data.copy()
    new_product_attributes_group_data1["name"] = f"{new_product_attributes_group_data1['name']}-1"
    new_product_attributes_group_data2["name"] = f"{new_product_attributes_group_data2['name']}-2"
    new_product_attributes_group_data1["order"] = 0
    new_product_attributes_group_data2["order"] = 1

    product_attributes_groups = plytix.products.attributes.groups.create_attributes_groups(
        [new_product_attributes_group_data1, new_product_attributes_group_data2]
    )

    assert len(product_attributes_groups) == 2

    assert product_attributes_groups[0].name == new_product_attributes_group_data1["name"]
    assert product_attributes_groups[0].attribute_labels == new_product_attributes_group_data1["attribute_labels"]
    assert product_attributes_groups[0].order == new_product_attributes_group_data1["order"]

    assert product_attributes_groups[1].name == new_product_attributes_group_data2["name"]
    assert product_attributes_groups[1].attribute_labels == new_product_attributes_group_data2["attribute_labels"]
    assert product_attributes_groups[1].order == new_product_attributes_group_data2["order"]
