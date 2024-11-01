from plytix_pim_client.dtos.filters import SearchFilter, OperatorEnum


async def test_convert_to_first_level_category(plytix_factory, new_product_category_data):
    parent_category = new_product_category_data.copy()
    subcategory = new_product_category_data.copy()
    parent_category["name"] = f"{parent_category['name']}-parent"
    subcategory["name"] = f"{subcategory['name']}-sub"
    parent_category = await plytix_factory.products.categories.create_product_category(**parent_category)
    subcategory = await plytix_factory.products.categories.create_product_category(
        parent_category_id=parent_category.id, **subcategory
    )

    subcategory = await plytix_factory.products.categories.convert_to_first_level_category(subcategory.id)

    assert subcategory.parents_ids == []


async def test_move_category(plytix_factory, new_product_category_data):
    parent_category = new_product_category_data.copy()
    subcategory = new_product_category_data.copy()
    parent_category["name"] = f"{parent_category['name']}-parent"
    subcategory["name"] = f"{subcategory['name']}-sub"
    parent_category = await plytix_factory.products.categories.create_product_category(**parent_category)
    subcategory = await plytix_factory.products.categories.create_product_category(
        parent_category_id=parent_category.id, **subcategory
    )
    new_parent_category = await plytix_factory.products.categories.create_product_category(**new_product_category_data)

    subcategory = await plytix_factory.products.categories.move_category(subcategory.id, new_parent_category.id)

    assert subcategory.parents_ids == [new_parent_category.id]


async def test_sorting_category(plytix_factory, product_category, product_subcategory, new_product_category_data):
    product_subcategory2 = new_product_category_data.copy()
    product_subcategory2["name"] = f"{product_subcategory2['name']}-sub2"
    product_subcategory2 = await plytix_factory.products.categories.create_product_category(
        parent_category_id=product_category.id, **product_subcategory2
    )

    await plytix_factory.products.categories.sorting_category(
        product_category.id, [product_subcategory2.id, product_subcategory.id]
    )

    categories = [
        _
        async for _ in plytix_factory.products.categories.search_all_product_categories(
            [
                [
                    SearchFilter(
                        field="id",
                        operator=OperatorEnum.IN,
                        value=[product_category.id, product_subcategory.id, product_subcategory2.id],
                    )
                ]
            ],
            ["id", "order", "n_children"],
            [],
            "id",
        )
    ][0]
    assert len(categories) == 3
    assert categories[0].id == product_subcategory2.id
    assert categories[1].id == product_subcategory.id
    assert categories[2].id == product_category.id
    assert categories[2].n_children == 2
    assert categories[1].order == "2"
    assert categories[2].order == "1"


async def test_sorting_root_category(plytix_factory, product_category, new_product_category_data):
    product_category2 = new_product_category_data.copy()
    product_category2["name"] = f"{product_category2['name']}-sub2"
    product_category2 = await plytix_factory.products.categories.create_product_category(**product_category2)

    await plytix_factory.products.categories.sorting_root_category([product_category2.id, product_category.id])

    categories = [
        _
        async for _ in plytix_factory.products.categories.search_all_product_categories(
            [
                [
                    SearchFilter(
                        field="id",
                        operator=OperatorEnum.IN,
                        value=[product_category.id, product_category2.id],
                    )
                ]
            ],
            ["id", "order"],
            [],
            "id",
        )
    ][0]
    assert len(categories) == 2
    assert categories[0].id == product_category2.id
    assert categories[1].id == product_category.id
    assert categories[0].order == "1"
    assert categories[1].order == "2"


async def test_convert_to_first_level_multiple_categories(plytix_factory, new_product_category_data):
    parent_category = new_product_category_data.copy()
    subcategory1 = new_product_category_data.copy()
    subcategory2 = new_product_category_data.copy()
    parent_category["name"] = f"{parent_category['name']}-parent"
    subcategory1["name"] = f"{subcategory1['name']}-sub1"
    subcategory2["name"] = f"{subcategory2['name']}-sub2"
    parent_category = await plytix_factory.products.categories.create_product_category(**parent_category)
    subcategory1 = await plytix_factory.products.categories.create_product_category(
        parent_category_id=parent_category.id, **subcategory1
    )
    subcategory2 = await plytix_factory.products.categories.create_product_category(
        parent_category_id=parent_category.id, **subcategory2
    )

    subcategories = await plytix_factory.products.categories.convert_to_first_level_categories(
        [subcategory1.id, subcategory2.id]
    )

    assert subcategories[0].parents_ids == []
    assert subcategories[1].parents_ids == []


async def test_move_multiple_categories(plytix_factory, new_product_category_data):
    parent_category1 = new_product_category_data.copy()
    parent_category2 = new_product_category_data.copy()
    subcategory1 = new_product_category_data.copy()
    subcategory2 = new_product_category_data.copy()
    parent_category1["name"] = f"{parent_category1['name']}-parent1"
    parent_category2["name"] = f"{parent_category2['name']}-parent2"
    subcategory1["name"] = f"{subcategory1['name']}-sub1"
    subcategory2["name"] = f"{subcategory2['name']}-sub2"
    parent_category1 = await plytix_factory.products.categories.create_product_category(**parent_category1)
    parent_category2 = await plytix_factory.products.categories.create_product_category(**parent_category2)
    subcategory1 = await plytix_factory.products.categories.create_product_category(
        parent_category_id=parent_category1.id, **subcategory1
    )
    subcategory2 = await plytix_factory.products.categories.create_product_category(
        parent_category_id=parent_category1.id, **subcategory2
    )

    subcategories = await plytix_factory.products.categories.move_categories(
        [(subcategory1.id, parent_category2.id), (subcategory2.id, parent_category2.id)],
    )

    assert subcategories[0].parents_ids == [parent_category2.id]
    assert subcategories[1].parents_ids == [parent_category2.id]