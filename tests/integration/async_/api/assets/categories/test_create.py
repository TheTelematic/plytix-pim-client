async def test_create_asset_category(plytix, new_asset_category_data):
    asset_category = await plytix.assets.categories.create_asset_category(**new_asset_category_data)
    assert asset_category.name == new_asset_category_data["name"]


async def test_create_asset_categories(plytix, new_asset_category_data):
    category1 = new_asset_category_data.copy()
    category2 = new_asset_category_data.copy()

    category1["name"] = f"{category1['name']}-1"
    category2["name"] = f"{category2['name']}-2"

    asset_categories = await plytix.assets.categories.create_asset_categories([category1, category2])
    assert asset_categories[0].name == new_asset_category_data["name"]
    assert asset_categories[1].name == new_asset_category_data["name"]
