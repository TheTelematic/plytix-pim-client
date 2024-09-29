import pytest


def test_convert_to_first_level_category(plytix, new_product_category_data):
    parent_category = new_product_category_data.copy()
    subcategory = new_product_category_data.copy()
    parent_category["name"] = f"{parent_category['name']}-parent"
    subcategory["name"] = f"{subcategory['name']}-sub"
    parent_category = plytix.products.categories.create_product_category(**parent_category)
    subcategory = plytix.products.categories.create_product_category(
        parent_category_id=parent_category.id, **subcategory
    )

    subcategory = plytix.products.categories.convert_to_first_level_category(subcategory.id)

    assert subcategory.parents_ids == []


def test_move_category(plytix, new_product_category_data):
    parent_category = new_product_category_data.copy()
    subcategory = new_product_category_data.copy()
    parent_category["name"] = f"{parent_category['name']}-parent"
    subcategory["name"] = f"{subcategory['name']}-sub"
    parent_category = plytix.products.categories.create_product_category(**parent_category)
    subcategory = plytix.products.categories.create_product_category(
        parent_category_id=parent_category.id, **subcategory
    )
    new_parent_category = plytix.products.categories.create_product_category(**new_product_category_data)

    subcategory = plytix.products.categories.move_category(subcategory.id, new_parent_category.id)

    assert subcategory.parents_ids == [new_parent_category.id]


def test_sorting_category(plytix, new_product_category_data):
    with pytest.raises(NotImplementedError):
        plytix.products.categories.sorting_category("category_id", ["subcategory_id"])


def test_sorting_root_category(plytix, new_product_category_data):
    with pytest.raises(NotImplementedError):
        plytix.products.categories.sorting_root_category(["subcategory_id"])


def test_convert_to_first_level_multiple_categories(plytix, new_product_category_data):
    parent_category = new_product_category_data.copy()
    subcategory1 = new_product_category_data.copy()
    subcategory2 = new_product_category_data.copy()
    parent_category["name"] = f"{parent_category['name']}-parent"
    subcategory1["name"] = f"{subcategory1['name']}-sub1"
    subcategory2["name"] = f"{subcategory2['name']}-sub2"
    parent_category = plytix.products.categories.create_product_category(**parent_category)
    subcategory1 = plytix.products.categories.create_product_category(
        parent_category_id=parent_category.id, **subcategory1
    )
    subcategory2 = plytix.products.categories.create_product_category(
        parent_category_id=parent_category.id, **subcategory2
    )

    subcategories = plytix.products.categories.convert_to_first_level_categories([subcategory1.id, subcategory2.id])

    assert subcategories[0].parents_ids == []
    assert subcategories[1].parents_ids == []


def test_move_multiple_categories(plytix, new_product_category_data):
    parent_category1 = new_product_category_data.copy()
    parent_category2 = new_product_category_data.copy()
    subcategory1 = new_product_category_data.copy()
    subcategory2 = new_product_category_data.copy()
    parent_category1["name"] = f"{parent_category1['name']}-parent1"
    parent_category2["name"] = f"{parent_category2['name']}-parent2"
    subcategory1["name"] = f"{subcategory1['name']}-sub1"
    subcategory2["name"] = f"{subcategory2['name']}-sub2"
    parent_category1 = plytix.products.categories.create_product_category(**parent_category1)
    parent_category2 = plytix.products.categories.create_product_category(**parent_category2)
    subcategory1 = plytix.products.categories.create_product_category(
        parent_category_id=parent_category1.id, **subcategory1
    )
    subcategory2 = plytix.products.categories.create_product_category(
        parent_category_id=parent_category1.id, **subcategory2
    )

    subcategories = plytix.products.categories.move_categories(
        [(subcategory1.id, parent_category2.id), (subcategory2.id, parent_category2.id)],
    )

    assert subcategories[0].parents_ids == [parent_category2.id]
    assert subcategories[1].parents_ids == [parent_category2.id]


def test_sorting_multiple_categories(plytix, new_product_category_data):
    with pytest.raises(NotImplementedError):
        plytix.products.categories.sorting_categories(
            [
                ("category_id", ["subcategory_id"]),
            ]
        )
