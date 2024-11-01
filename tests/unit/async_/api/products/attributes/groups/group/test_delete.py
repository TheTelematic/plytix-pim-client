async def test_delete_attributes_group(plytix_factory, new_product_attributes_group_data):
    product_attributes_group = await plytix_factory.products.attributes.groups.create_attributes_group(
        **new_product_attributes_group_data
    )
    assert product_attributes_group.id

    deleted = await plytix_factory.products.attributes.groups.delete_attributes_group(product_attributes_group.id)
    assert deleted


async def test_delete_attributes_group_that_does_not_exist(plytix_factory):
    deleted = await plytix_factory.products.attributes.groups.delete_attributes_group("non_existent_id")
    assert not deleted


async def test_delete_attributes_groups(plytix_factory, new_product_attributes_group_data):
    attribute1 = new_product_attributes_group_data.copy()
    attribute2 = new_product_attributes_group_data.copy()
    attribute3 = new_product_attributes_group_data.copy()

    attribute1["name"] = f"{attribute1['name']}-1"
    attribute2["name"] = f"{attribute2['name']}-2"
    attribute3["name"] = f"{attribute3['name']}-3"

    product_attributes_groups = [
        await plytix_factory.products.attributes.groups.create_attributes_group(**attribute1),
        await plytix_factory.products.attributes.groups.create_attributes_group(**attribute2),
        await plytix_factory.products.attributes.groups.create_attributes_group(**attribute3),
    ]
    assert all(product_attributes_group.id for product_attributes_group in product_attributes_groups)

    deleted = await plytix_factory.products.attributes.groups.delete_attributes_groups(
        [product_attributes_group.id for product_attributes_group in product_attributes_groups]
    )
    assert all(deleted)
