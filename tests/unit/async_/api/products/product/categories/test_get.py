async def test_get_one_category(plytix_factory, product, product_category):
    await plytix_factory.products.categories.link_product_to_category(product.id, product_category.id)

    categories = await plytix_factory.products.categories.get_product_categories(product.id, product_category.id)

    assert len(categories) == 1
    assert categories[0].id == product_category.id
    assert categories[0].name == product_category.name
    assert categories[0].path == product_category.path


async def test_get_one_category_of_multiple_products(
    plytix_factory, product, product_category, new_product_data, new_product_category_data
):
    product2 = new_product_data.copy()
    product2["sku"] = f"{product2['sku']}-2"
    product2 = await plytix_factory.products.create_product(**product2)
    product_category2 = new_product_category_data.copy()
    product_category2["name"] = f"{product_category2['name']}-2"
    product_category2 = await plytix_factory.products.categories.create_product_category(**product_category2)
    await plytix_factory.products.categories.link_product_to_categories(
        [
            (product.id, product_category.id),
            (product2.id, product_category2.id),
        ]
    )

    categories_groups = await plytix_factory.products.categories.get_multiple_product_categories(
        [
            (product.id, product_category.id),
            (product2.id, product_category2.id),
        ]
    )

    assert len(categories_groups) == 2
    assert len(categories_groups[0]) == 1
    assert len(categories_groups[1]) == 1
    assert categories_groups[0][0].id == product_category.id
    assert categories_groups[0][0].name == product_category.name
    assert categories_groups[0][0].path == product_category.path
    assert categories_groups[1][0].id == product_category2.id
    assert categories_groups[1][0].name == product_category2.name
    assert categories_groups[1][0].path == product_category2.path


async def test_get_not_existing_category(plytix_factory):
    categories = await plytix_factory.products.categories.get_product_categories("not-existing", "not-existing")

    assert categories is None


async def test_get_not_existing_category_of_multiple_products(plytix_factory):
    categories_groups = await plytix_factory.products.categories.get_multiple_product_categories(
        [
            ("not-existing", "not-existing"),
            ("not-existing", "not-existing"),
        ]
    )

    assert categories_groups == [None, None]


async def test_get_all_categories_for_one_product(plytix_factory, product, product_category, new_product_category_data):
    product_category2 = new_product_category_data.copy()
    product_category2["name"] = f"{product_category2['name']}-2"
    product_category2 = await plytix_factory.products.categories.create_product_category(**product_category2)
    await plytix_factory.products.categories.link_product_to_categories(
        [
            (product.id, product_category.id),
            (product.id, product_category2.id),
        ]
    )

    categories = await plytix_factory.products.categories.get_product_categories(product.id)

    assert len(categories) == 2
    assert categories[0].id == product_category.id
    assert categories[0].name == product_category.name
    assert categories[0].path == product_category.path
    assert categories[1].id == product_category2.id
    assert categories[1].name == product_category2.name
    assert categories[1].path == product_category2.path


async def test_get_all_categories_for_multiple_products(
    plytix_factory, product, product_category, new_product_data, new_product_category_data
):
    product2 = new_product_data.copy()
    product2["sku"] = f"{product2['sku']}-2"
    product2 = await plytix_factory.products.create_product(**product2)
    product_category2 = new_product_category_data.copy()
    product_category2["name"] = f"{product_category2['name']}-2"
    product_category2 = await plytix_factory.products.categories.create_product_category(**product_category2)
    await plytix_factory.products.categories.link_product_to_categories(
        [
            (product.id, product_category.id),
            (product.id, product_category2.id),
            (product2.id, product_category.id),
            (product2.id, product_category2.id),
        ]
    )

    categories_groups = await plytix_factory.products.categories.get_multiple_product_categories(
        [
            (product.id, None),
            (product2.id, None),
        ]
    )

    assert len(categories_groups) == 2
    assert len(categories_groups[0]) == 2
    assert len(categories_groups[1]) == 2
    assert categories_groups[0][0].id == product_category.id
    assert categories_groups[0][0].name == product_category.name
    assert categories_groups[0][0].path == product_category.path
    assert categories_groups[0][1].id == product_category2.id
    assert categories_groups[0][1].name == product_category2.name
    assert categories_groups[0][1].path == product_category2.path
    assert categories_groups[1][0].id == product_category.id
    assert categories_groups[1][0].name == product_category.name
    assert categories_groups[1][0].path == product_category.path
    assert categories_groups[1][1].id == product_category2.id
    assert categories_groups[1][1].name == product_category2.name
    assert categories_groups[1][1].path == product_category2.path
