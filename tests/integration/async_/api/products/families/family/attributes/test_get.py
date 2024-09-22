from plytix_pim_client.dtos.products.family import ProductAttributeFamilyLevel


async def test_get_family_attributes(plytix, new_product_family_data, new_product_attribute_data):
    family = await plytix.products.families.create_family(**new_product_family_data)
    attribute = await plytix.products.attributes.create_attribute(**new_product_attribute_data)
    await plytix.products.families.link_attribute_to_family(family.id, [attribute.id])

    results = await plytix.products.families.attributes.get_family_attributes(family.id)

    assert len(results) == 1
    assert results[0].id == attribute.id
    assert results[0].name == attribute.name
    assert results[0].label == attribute.label
    assert results[0].attribute_level == ProductAttributeFamilyLevel.OFF


async def test_get_family_attributes_not_found(plytix):
    results = await plytix.products.families.attributes.get_family_attributes("not-found")
    assert results is None


async def test_get_families_attributes(plytix, new_product_family_data, new_product_attribute_data):
    family1 = new_product_family_data.copy()
    family2 = new_product_family_data.copy()
    family1["name"] = f"{family1['name']} 1"
    family2["name"] = f"{family2['name']} 2"
    family1 = await plytix.products.families.create_family(**family1)
    family2 = await plytix.products.families.create_family(**family2)

    attribute1 = new_product_attribute_data.copy()
    attribute2 = new_product_attribute_data.copy()
    attribute1["name"] = f"{attribute1['name']} 1"
    attribute2["name"] = f"{attribute2['name']} 2"
    attribute1 = await plytix.products.attributes.create_attribute(**attribute1)
    attribute2 = await plytix.products.attributes.create_attribute(**attribute2)

    await plytix.products.families.link_attribute_to_family(family1.id, [attribute1.id])
    await plytix.products.families.link_attribute_to_family(family2.id, [attribute2.id])

    results = await plytix.products.families.attributes.get_families_attributes([family1.id, family2.id])

    assert len(results) == 2
    assert len(results[0]) == 1
    assert results[0][0].id == attribute1.id
    assert results[0][0].name == attribute1.name
    assert results[0][0].label == attribute1.label
    assert results[0][0].attribute_level == ProductAttributeFamilyLevel.OFF
    assert len(results[1]) == 1
    assert results[1][0].id == attribute2.id
    assert results[1][0].name == attribute2.name
    assert results[1][0].label == attribute2.label
    assert results[1][0].attribute_level == ProductAttributeFamilyLevel.OFF
