def test_delete_product_category(plytix, new_product_category_data):
    product_category = plytix.products.categories.create_product_category(**new_product_category_data)

    result = plytix.products.categories.delete_product_category(product_category.id)

    assert result is True


def test_delete_product_category_with_non_existent_category(plytix):
    result = plytix.products.categories.delete_product_category("non-existent-id")

    assert result is False


def test_delete_product_categories(plytix, new_product_category_data):
    category1 = new_product_category_data.copy()
    category2 = new_product_category_data.copy()
    category1["name"] = f"{category1['name']} 1"
    category2["name"] = f"{category2['name']} 2"
    category1 = plytix.products.categories.create_product_category(**category1)
    category2 = plytix.products.categories.create_product_category(**category2)

    result = plytix.products.categories.delete_product_categories([category1.id, category2.id])

    assert result == [True, True]
