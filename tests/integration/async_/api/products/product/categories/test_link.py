async def test_link_category_to_product(plytix, product, product_category):
    result = await plytix.products.categories.link_product_to_category(product.id, product_category.id)

    assert result.id == product_category.id
    product = await plytix.products.get_product(product.id)
    assert product.categories == [
        {"id": product_category.id, "name": product_category.name, "path": product_category.path}
    ]
