async def test_create_product_category(plytix_factory, new_product_category_data):
    product_category = await plytix_factory.products.categories.create_product_category(**new_product_category_data)
    assert product_category.name == new_product_category_data["name"]


async def test_create_product_subcategory(plytix_factory, new_product_category_data):
    parent_category = await plytix_factory.products.categories.create_product_category(**new_product_category_data)
    subcategory_data = new_product_category_data.copy()
    subcategory_data["name"] = f"{subcategory_data['name']}-sub"

    subcategory = await plytix_factory.products.categories.create_product_category(
        **subcategory_data, parent_category_id=parent_category.id
    )

    assert subcategory.name == subcategory_data["name"]
    assert subcategory.parents_ids == [parent_category.id]


async def test_create_product_categories(plytix_factory, new_product_category_data):
    category1 = new_product_category_data.copy()
    category2 = new_product_category_data.copy()

    category1["name"] = f"{category1['name']}-1"
    category2["name"] = f"{category2['name']}-2"

    product_categories = await plytix_factory.products.categories.create_product_categories([category1, category2])
    assert product_categories[0].name == category1["name"]
    assert product_categories[1].name == category2["name"]


async def test_create_product_subcategories(plytix_factory, new_product_category_data):
    parent_category = await plytix_factory.products.categories.create_product_category(**new_product_category_data)
    subcategory1_data = new_product_category_data.copy()
    subcategory2_data = new_product_category_data.copy()

    subcategory1_data["name"] = f"{subcategory1_data['name']}-sub1"
    subcategory2_data["name"] = f"{subcategory2_data['name']}-sub2"
    subcategory1_data["parent_category_id"] = parent_category.id
    subcategory2_data["parent_category_id"] = parent_category.id

    subcategories = await plytix_factory.products.categories.create_product_categories([subcategory1_data, subcategory2_data])

    assert subcategories[0].name == subcategory1_data["name"]
    assert subcategories[0].parents_ids == [parent_category.id]
    assert subcategories[1].name == subcategory2_data["name"]
    assert subcategories[1].parents_ids == [parent_category.id]
