async def test_delete_asset_category(plytix_factory, new_asset_category_data):
    asset_category = await plytix_factory.assets.categories.create_asset_category(**new_asset_category_data)

    result = await plytix_factory.assets.categories.delete_asset_category(asset_category.id)

    assert result is True


async def test_delete_asset_category_with_non_existent_category(plytix_factory):
    result = await plytix_factory.assets.categories.delete_asset_category("non-existent-id")

    assert result is False


async def test_delete_asset_categories(plytix_factory, new_asset_category_data):
    category1 = new_asset_category_data.copy()
    category2 = new_asset_category_data.copy()
    category1["name"] = f"{category1['name']} 1"
    category2["name"] = f"{category2['name']} 2"
    category1 = await plytix_factory.assets.categories.create_asset_category(**category1)
    category2 = await plytix_factory.assets.categories.create_asset_category(**category2)

    result = await plytix_factory.assets.categories.delete_asset_categories([category1.id, category2.id])

    assert result == [True, True]
