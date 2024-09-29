async def test_unlink_category_to_product(plytix, product, product_category):
    await plytix.products.categories.link_product_to_category(product.id, product_category.id)

    result = await plytix.products.categories.unlink_product_to_category(product.id, product_category.id)

    assert result is True
    product = await plytix.products.get_product(product.id)
    assert product.categories == []


async def test_unlink_not_existing_product(plytix):
    result = await plytix.products.categories.unlink_product_to_category("not-existing", "not-existing")

    assert result is False


async def test_multiple_products_to_categories(
    plytix, product, product_category, new_product_data, new_product_category_data
):
    product2 = new_product_data.copy()
    product2["sku"] = f"{product2['sku']}-2"
    product2 = await plytix.products.create_product(**product2)
    product_category2 = new_product_category_data.copy()
    product_category2["name"] = f"{product_category2['name']}-2"
    product_category2 = await plytix.products.categories.create_product_category(**product_category2)
    await plytix.products.categories.link_product_to_categories(
        [
            (product.id, product_category.id),
            (product2.id, product_category2.id),
        ]
    )

    results = await plytix.products.categories.unlink_product_to_categories(
        [
            (product.id, product_category.id),
            (product2.id, product_category2.id),
        ]
    )

    assert results == [True, True]
    product = await plytix.products.get_product(product.id)
    product2 = await plytix.products.get_product(product2.id)
    assert product.categories == []
    assert product2.categories == []
