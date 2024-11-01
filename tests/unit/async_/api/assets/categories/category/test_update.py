from plytix_pim_client.dtos.filters import SearchFilter, OperatorEnum


async def test_convert_to_first_level_category(plytix_factory, new_asset_category_data):
    parent_category = new_asset_category_data.copy()
    subcategory = new_asset_category_data.copy()
    parent_category["name"] = f"{parent_category['name']}-parent"
    subcategory["name"] = f"{subcategory['name']}-sub"
    parent_category = await plytix_factory.assets.categories.create_asset_category(**parent_category)
    subcategory = await plytix_factory.assets.categories.create_asset_category(
        parent_category_id=parent_category.id, **subcategory
    )

    subcategory = await plytix_factory.assets.categories.convert_to_first_level_category(subcategory.id)

    assert subcategory.parents_ids == []


async def test_move_category(plytix_factory, new_asset_category_data):
    parent_category = new_asset_category_data.copy()
    subcategory = new_asset_category_data.copy()
    parent_category["name"] = f"{parent_category['name']}-parent"
    subcategory["name"] = f"{subcategory['name']}-sub"
    parent_category = await plytix_factory.assets.categories.create_asset_category(**parent_category)
    subcategory = await plytix_factory.assets.categories.create_asset_category(
        parent_category_id=parent_category.id, **subcategory
    )
    new_parent_category = await plytix_factory.assets.categories.create_asset_category(**new_asset_category_data)

    subcategory = await plytix_factory.assets.categories.move_category(subcategory.id, new_parent_category.id)

    assert subcategory.parents_ids == [new_parent_category.id]


async def test_sorting_category(plytix_factory, asset_category, asset_subcategory, new_asset_category_data):
    asset_subcategory2 = new_asset_category_data.copy()
    asset_subcategory2["name"] = f"{asset_subcategory2['name']}-sub2"
    asset_subcategory2 = await plytix_factory.assets.categories.create_asset_category(
        parent_category_id=asset_category.id, **asset_subcategory2
    )

    await plytix_factory.assets.categories.sorting_category(asset_category.id, [asset_subcategory2.id, asset_subcategory.id])

    categories = [
        _
        async for _ in plytix_factory.assets.categories.search_all_asset_categories(
            [
                [
                    SearchFilter(
                        field="id",
                        operator=OperatorEnum.IN,
                        value=[asset_category.id, asset_subcategory.id, asset_subcategory2.id],
                    )
                ]
            ],
            ["id", "order", "n_children"],
            [],
            "id",
        )
    ][0]
    assert len(categories) == 3
    assert categories[0].id == asset_subcategory2.id
    assert categories[1].id == asset_subcategory.id
    assert categories[2].id == asset_category.id
    assert categories[2].n_children == 2
    assert categories[1].order == "2"
    assert categories[2].order == "1"


async def test_sorting_root_category(plytix_factory, asset_category, new_asset_category_data):
    asset_category2 = new_asset_category_data.copy()
    asset_category2["name"] = f"{asset_category2['name']}-sub2"
    asset_category2 = await plytix_factory.assets.categories.create_asset_category(**asset_category2)

    await plytix_factory.assets.categories.sorting_root_category([asset_category2.id, asset_category.id])

    categories = [
        _
        async for _ in plytix_factory.assets.categories.search_all_asset_categories(
            [
                [
                    SearchFilter(
                        field="id",
                        operator=OperatorEnum.IN,
                        value=[asset_category.id, asset_category2.id],
                    )
                ]
            ],
            ["id", "order"],
            [],
            "id",
        )
    ][0]
    assert len(categories) == 2
    assert categories[0].id == asset_category2.id
    assert categories[1].id == asset_category.id
    assert categories[0].order == "1"
    assert categories[1].order == "2"


async def test_convert_to_first_level_multiple_categories(plytix_factory, new_asset_category_data):
    parent_category = new_asset_category_data.copy()
    subcategory1 = new_asset_category_data.copy()
    subcategory2 = new_asset_category_data.copy()
    parent_category["name"] = f"{parent_category['name']}-parent"
    subcategory1["name"] = f"{subcategory1['name']}-sub1"
    subcategory2["name"] = f"{subcategory2['name']}-sub2"
    parent_category = await plytix_factory.assets.categories.create_asset_category(**parent_category)
    subcategory1 = await plytix_factory.assets.categories.create_asset_category(
        parent_category_id=parent_category.id, **subcategory1
    )
    subcategory2 = await plytix_factory.assets.categories.create_asset_category(
        parent_category_id=parent_category.id, **subcategory2
    )

    subcategories = await plytix_factory.assets.categories.convert_to_first_level_categories([subcategory1.id, subcategory2.id])

    assert subcategories[0].parents_ids == []
    assert subcategories[1].parents_ids == []


async def test_move_multiple_categories(plytix_factory, new_asset_category_data):
    parent_category1 = new_asset_category_data.copy()
    parent_category2 = new_asset_category_data.copy()
    subcategory1 = new_asset_category_data.copy()
    subcategory2 = new_asset_category_data.copy()
    parent_category1["name"] = f"{parent_category1['name']}-parent1"
    parent_category2["name"] = f"{parent_category2['name']}-parent2"
    subcategory1["name"] = f"{subcategory1['name']}-sub1"
    subcategory2["name"] = f"{subcategory2['name']}-sub2"
    parent_category1 = await plytix_factory.assets.categories.create_asset_category(**parent_category1)
    parent_category2 = await plytix_factory.assets.categories.create_asset_category(**parent_category2)
    subcategory1 = await plytix_factory.assets.categories.create_asset_category(
        parent_category_id=parent_category1.id, **subcategory1
    )
    subcategory2 = await plytix_factory.assets.categories.create_asset_category(
        parent_category_id=parent_category1.id, **subcategory2
    )

    subcategories = await plytix_factory.assets.categories.move_categories(
        [(subcategory1.id, parent_category2.id), (subcategory2.id, parent_category2.id)],
    )

    assert subcategories[0].parents_ids == [parent_category2.id]
    assert subcategories[1].parents_ids == [parent_category2.id]
