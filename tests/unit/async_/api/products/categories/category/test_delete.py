async def test_delete_product_category(plytix_factory, new_product_category_data):
    product_category = await plytix_factory.products.categories.create_product_category(**new_product_category_data)

    result = await plytix_factory.products.categories.delete_product_category(product_category.id)

    assert result is True


async def test_delete_product_category_with_non_existent_category(plytix_factory):
    result = await plytix_factory.products.categories.delete_product_category("non-existent-id")

    assert result is False


async def test_delete_product_categories(plytix_factory, new_product_category_data):
    category1 = new_product_category_data.copy()
    category2 = new_product_category_data.copy()
    category1["name"] = f"{category1['name']} 1"
    category2["name"] = f"{category2['name']} 2"
    category1 = await plytix_factory.products.categories.create_product_category(**category1)
    category2 = await plytix_factory.products.categories.create_product_category(**category2)

    result = await plytix_factory.products.categories.delete_product_categories([category1.id, category2.id])

    assert result == [True, True]
