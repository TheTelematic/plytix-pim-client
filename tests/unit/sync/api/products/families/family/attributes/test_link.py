from plytix_pim_client.dtos.products.family import ProductAttributeFamilyLevel


def test_link_attribute_to_family(plytix, new_product_family_data, new_product_attribute_data):
    new_family = plytix.products.families.create_family(**new_product_family_data)
    new_attribute = plytix.products.attributes.create_attribute(**new_product_attribute_data)

    result = plytix.products.families.attributes.link_attribute_to_family(new_family.id, [new_attribute.id])

    assert result is True
    family = plytix.products.families.get_family(new_family.id)
    assert family.total_attributes == 1
    attributes = plytix.products.families.attributes.get_family_attributes(new_family.id)
    assert len(attributes) == 1
    assert attributes[0].id == new_attribute.id


def test_link_attributes_to_families(plytix, new_product_family_data, new_product_attribute_data):
    family1 = new_product_family_data.copy()
    family2 = new_product_family_data.copy()
    family1["name"] = f"{new_product_family_data['name']}-1"
    family2["name"] = f"{new_product_family_data['name']}-2"

    attribute1 = new_product_attribute_data.copy()
    attribute2 = new_product_attribute_data.copy()
    attribute1["name"] = f"{new_product_attribute_data['name']}-1"
    attribute2["name"] = f"{new_product_attribute_data['name']}-2"

    new_family1 = plytix.products.families.create_family(**family1)
    new_family2 = plytix.products.families.create_family(**family2)
    new_attribute1 = plytix.products.attributes.create_attribute(**attribute1)
    new_attribute2 = plytix.products.attributes.create_attribute(**attribute2)

    result = plytix.products.families.attributes.link_attributes_to_families(
        [
            (new_family1.id, [new_attribute1.id], ProductAttributeFamilyLevel.OFF),
            (new_family2.id, [new_attribute2.id], ProductAttributeFamilyLevel.ON),
        ]
    )

    assert result == [True, True]
    family1 = plytix.products.families.get_family(new_family1.id)
    family2 = plytix.products.families.get_family(new_family2.id)
    assert family1.total_attributes == 1
    assert family2.total_attributes == 1
    attributes1 = plytix.products.families.attributes.get_family_attributes(new_family1.id)
    attributes2 = plytix.products.families.attributes.get_family_attributes(new_family2.id)
    assert len(attributes1) == 1
    assert len(attributes2) == 1
    assert attributes1[0].id == new_attribute1.id
    assert attributes2[0].id == new_attribute2.id
    assert attributes1[0].attribute_level == ProductAttributeFamilyLevel.OFF
    assert attributes2[0].attribute_level == ProductAttributeFamilyLevel.ON