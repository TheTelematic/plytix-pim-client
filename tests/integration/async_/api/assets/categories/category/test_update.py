import pytest


async def test_convert_to_first_level_category(plytix, new_asset_category_data):
    parent_category = new_asset_category_data.copy()
    subcategory = new_asset_category_data.copy()
    parent_category["name"] = f"{parent_category['name']}-parent"
    subcategory["name"] = f"{subcategory['name']}-sub"
    parent_category = await plytix.assets.categories.create_asset_category(**parent_category)
    subcategory = await plytix.assets.categories.create_asset_category(
        parent_category_id=parent_category.id, **subcategory
    )

    subcategory = await plytix.assets.categories.convert_to_first_level_category(subcategory.id)

    assert subcategory.parents_ids == []


async def test_move_category(plytix, new_asset_category_data):
    parent_category = new_asset_category_data.copy()
    subcategory = new_asset_category_data.copy()
    parent_category["name"] = f"{parent_category['name']}-parent"
    subcategory["name"] = f"{subcategory['name']}-sub"
    parent_category = await plytix.assets.categories.create_asset_category(**parent_category)
    subcategory = await plytix.assets.categories.create_asset_category(
        parent_category_id=parent_category.id, **subcategory
    )
    new_parent_category = await plytix.assets.categories.create_asset_category(**new_asset_category_data)

    subcategory = await plytix.assets.categories.move_category(subcategory.id, new_parent_category.id)

    assert subcategory.parents_ids == [new_parent_category.id]


async def test_sorting_category(plytix, new_asset_category_data):
    with pytest.raises(NotImplementedError):
        await plytix.assets.categories.sorting_category("category_id", ["subcategory_id"])


async def test_sorting_root_category(plytix, new_asset_category_data):
    with pytest.raises(NotImplementedError):
        await plytix.assets.categories.sorting_root_category(["subcategory_id"])


async def test_convert_to_first_level_multiple_categories(plytix, new_asset_category_data):
    parent_category = new_asset_category_data.copy()
    subcategory1 = new_asset_category_data.copy()
    subcategory2 = new_asset_category_data.copy()
    parent_category["name"] = f"{parent_category['name']}-parent"
    subcategory1["name"] = f"{subcategory1['name']}-sub1"
    subcategory2["name"] = f"{subcategory2['name']}-sub2"
    parent_category = await plytix.assets.categories.create_asset_category(**parent_category)
    subcategory1 = await plytix.assets.categories.create_asset_category(
        parent_category_id=parent_category.id, **subcategory1
    )
    subcategory2 = await plytix.assets.categories.create_asset_category(
        parent_category_id=parent_category.id, **subcategory2
    )

    subcategories = await plytix.assets.categories.convert_to_first_level_categories([subcategory1.id, subcategory2.id])

    assert subcategories[0].parents_ids == []
    assert subcategories[1].parents_ids == []


async def test_move_multiple_categories(plytix, new_asset_category_data):
    parent_category1 = new_asset_category_data.copy()
    parent_category2 = new_asset_category_data.copy()
    subcategory1 = new_asset_category_data.copy()
    subcategory2 = new_asset_category_data.copy()
    parent_category1["name"] = f"{parent_category1['name']}-parent1"
    parent_category2["name"] = f"{parent_category2['name']}-parent2"
    subcategory1["name"] = f"{subcategory1['name']}-sub1"
    subcategory2["name"] = f"{subcategory2['name']}-sub2"
    parent_category1 = await plytix.assets.categories.create_asset_category(**parent_category1)
    parent_category2 = await plytix.assets.categories.create_asset_category(**parent_category2)
    subcategory1 = await plytix.assets.categories.create_asset_category(
        parent_category_id=parent_category1.id, **subcategory1
    )
    subcategory2 = await plytix.assets.categories.create_asset_category(
        parent_category_id=parent_category1.id, **subcategory2
    )

    subcategories = await plytix.assets.categories.move_categories(
        [(subcategory1.id, parent_category2.id), (subcategory2.id, parent_category2.id)],
    )

    assert subcategories[0].parents_ids == [parent_category2.id]
    assert subcategories[1].parents_ids == [parent_category2.id]


async def test_sorting_multiple_categories(plytix, new_asset_category_data):
    with pytest.raises(NotImplementedError):
        await plytix.assets.categories.sorting_categories(
            [
                ("category_id", ["subcategory_id"]),
            ]
        )
