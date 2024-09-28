def test_delete_asset_category(plytix, new_asset_category_data):
    asset_category = plytix.assets.categories.create_asset_category(**new_asset_category_data)

    result = plytix.assets.categories.delete_asset_category(asset_category.id)

    assert result is True


def test_delete_asset_category_with_non_existent_category(plytix):
    result = plytix.assets.categories.delete_asset_category("non-existent-id")

    assert result is False


def test_delete_asset_categories(plytix, new_asset_category_data):
    category1 = new_asset_category_data.copy()
    category2 = new_asset_category_data.copy()
    category1["name"] = f"{category1['name']} 1"
    category2["name"] = f"{category2['name']} 2"
    category1 = plytix.assets.categories.create_asset_category(**category1)
    category2 = plytix.assets.categories.create_asset_category(**category2)

    result = plytix.assets.categories.delete_asset_categories([category1.id, category2.id])

    assert result == [True, True]
