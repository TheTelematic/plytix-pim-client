def test_create_asset_category(plytix, new_asset_category_data):
    asset_category = plytix.assets.categories.create_asset_category(**new_asset_category_data)
    assert asset_category.name == new_asset_category_data["name"]


def test_create_asset_subcategory(plytix, new_asset_category_data):
    parent_category = plytix.assets.categories.create_asset_category(**new_asset_category_data)
    subcategory_data = new_asset_category_data.copy()
    subcategory_data["name"] = f"{subcategory_data['name']}-sub"

    subcategory = plytix.assets.categories.create_asset_category(
        **subcategory_data, parent_category_id=parent_category.id
    )

    assert subcategory.name == subcategory_data["name"]
    assert subcategory.parents_ids == [parent_category.id]


def test_create_asset_categories(plytix, new_asset_category_data):
    category1 = new_asset_category_data.copy()
    category2 = new_asset_category_data.copy()

    category1["name"] = f"{category1['name']}-1"
    category2["name"] = f"{category2['name']}-2"

    asset_categories = plytix.assets.categories.create_asset_categories([category1, category2])
    assert asset_categories[0].name == category1["name"]
    assert asset_categories[1].name == category2["name"]


def test_create_asset_subcategories(plytix, new_asset_category_data):
    parent_category = plytix.assets.categories.create_asset_category(**new_asset_category_data)
    subcategory1_data = new_asset_category_data.copy()
    subcategory2_data = new_asset_category_data.copy()

    subcategory1_data["name"] = f"{subcategory1_data['name']}-sub1"
    subcategory2_data["name"] = f"{subcategory2_data['name']}-sub2"
    subcategory1_data["parent_category_id"] = parent_category.id
    subcategory2_data["parent_category_id"] = parent_category.id

    subcategories = plytix.assets.categories.create_asset_categories([subcategory1_data, subcategory2_data])

    assert subcategories[0].name == subcategory1_data["name"]
    assert subcategories[0].parents_ids == [parent_category.id]
    assert subcategories[1].name == subcategory2_data["name"]
    assert subcategories[1].parents_ids == [parent_category.id]
