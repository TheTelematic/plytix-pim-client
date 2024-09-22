import asyncio

from plytix_pim_client.dtos.products.family import ProductAttributeFamilyLevel


async def test_edit_inheritance(plytix, new_product_family_data, new_product_attribute_data):
    new_family = await plytix.products.families.create_family(**new_product_family_data)
    new_attribute = await plytix.products.attributes.create_attribute(**new_product_attribute_data)
    await plytix.products.families.attributes.link_attribute_to_family(new_family.id, [new_attribute.id])

    result = await plytix.products.families.attributes.edit_attributes_inheritance(
        new_family.id, [new_attribute.label], []
    )
    await asyncio.sleep(1)

    assert result is True
    family = await plytix.products.families.get_family(new_family.id)
    assert family.total_attributes == 1
    attributes = await plytix.products.families.attributes.get_family_attributes(new_family.id)
    assert len(attributes) == 1
    assert attributes[0].id == new_attribute.id
    assert attributes[0].attribute_level == ProductAttributeFamilyLevel.ON


async def test_edit_inheritance_with_no_level(plytix, new_product_family_data, new_product_attribute_data):
    new_family = await plytix.products.families.create_family(**new_product_family_data)
    new_attribute = await plytix.products.attributes.create_attribute(**new_product_attribute_data)
    await plytix.products.families.attributes.link_attribute_to_family(new_family.id, [new_attribute.id])

    result = await plytix.products.families.attributes.edit_attributes_inheritance(
        new_family.id, [], [new_attribute.label]
    )
    await asyncio.sleep(1)

    assert result is True
    family = await plytix.products.families.get_family(new_family.id)
    assert family.total_attributes == 1
    attributes = await plytix.products.families.attributes.get_family_attributes(new_family.id)
    assert len(attributes) == 1
    assert attributes[0].id == new_attribute.id
    assert attributes[0].attribute_level == ProductAttributeFamilyLevel.OFF


async def test_edit_multiple_inheritance(plytix, new_product_family_data, new_product_attribute_data):
    new_family = await plytix.products.families.create_family(**new_product_family_data)
    attribute1 = new_product_attribute_data.copy()
    attribute2 = new_product_attribute_data.copy()
    attribute1["name"] = f"{new_product_attribute_data['name']}-1"
    attribute2["name"] = f"{new_product_attribute_data['name']}-2"
    new_attribute1 = await plytix.products.attributes.create_attribute(**attribute1)
    new_attribute2 = await plytix.products.attributes.create_attribute(**attribute2)
    await plytix.products.families.attributes.link_attribute_to_family(
        new_family.id, [new_attribute1.id, new_attribute2.id], ProductAttributeFamilyLevel.ON
    )

    result = await plytix.products.families.attributes.edit_attributes_inheritances(
        [(new_family.id, [new_attribute1.label], [new_attribute2.label])]
    )
    await asyncio.sleep(1)

    assert result == [True]
    family = await plytix.products.families.get_family(new_family.id)
    assert family.total_attributes == 2
    attributes = await plytix.products.families.attributes.get_family_attributes(new_family.id)
    assert len(attributes) == 2
    assert new_attribute1.id in [attribute.id for attribute in attributes]
    assert new_attribute2.id in [attribute.id for attribute in attributes]
    assert all(
        (
            attribute.attribute_level == ProductAttributeFamilyLevel.OFF
            if attribute.id == new_attribute2.id
            else attribute.attribute_level == ProductAttributeFamilyLevel.ON
        )
        for attribute in attributes
    )
