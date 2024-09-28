from plytix_pim_client import SearchFilter, OperatorEnum


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
    parent_category = new_asset_category_data.copy()
    subcategory_data1 = new_asset_category_data.copy()
    subcategory_data2 = new_asset_category_data.copy()
    parent_category["name"] = f"{parent_category['name']}-parent"
    subcategory_data1["name"] = f"{subcategory_data1['name']}-sub1"
    subcategory_data2["name"] = f"{subcategory_data2['name']}-sub2"
    parent_category = await plytix.assets.categories.create_asset_category(**parent_category)
    subcategory1 = await plytix.assets.categories.create_asset_category(
        parent_category_id=parent_category.id, **subcategory_data1
    )
    subcategory2 = await plytix.assets.categories.create_asset_category(
        parent_category_id=parent_category.id, **subcategory_data2
    )

    await plytix.assets.categories.sorting_category(parent_category.id, [subcategory2.id, subcategory1.id])

    subcategories = []
    async for categories in plytix.assets.categories.search_all_asset_categories(
        [[SearchFilter(field="id", operator=OperatorEnum.IN, value=[subcategory2.id, subcategory1.id])]],
        ["id", "order"],
        [],
        "id",
        False,
    ):
        subcategories.extend(categories)

    assert subcategories[0].id == subcategory2.id
    assert subcategories[1].id == subcategory1.id
    assert int(subcategories[0].order) == 1
    assert int(subcategories[1].order) == 2


async def test_sorting_root_category(plytix, new_asset_category_data): ...


async def test_convert_to_first_level_multiple_categories(plytix, new_asset_category_data): ...


async def test_move_multiple_categories(plytix, new_asset_category_data): ...


async def test_sorting_multiple_categories(plytix, new_asset_category_data): ...
