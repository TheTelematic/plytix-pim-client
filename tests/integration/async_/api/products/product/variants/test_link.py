async def test_link_variant_to_product(
    plytix,
    product,
    new_product_data,
):
    new_product_data["sku"] = f"{new_product_data['sku']}-variant"
    product_variant = await plytix.products.create_product(**new_product_data)

    result = await plytix.products.variants.link_variant_to_product(product.id, product_variant.id)

    assert result is True


async def test_link_variant_to_product_not_found(plytix):
    result = await plytix.products.variants.link_variant_to_product("not_found", "not_found")

    assert result is False


async def test_link_variants_to_products(plytix, product, new_product_data):
    product_variant_data = new_product_data.copy()
    product_variant_data["sku"] = f"{new_product_data['sku']}-variant"
    product_variant = await plytix.products.create_product(**product_variant_data)
    product2 = new_product_data.copy()
    product2["sku"] = f"{new_product_data['sku']}-2"
    product2 = await plytix.products.create_product(**product2)
    product_variant_data2 = new_product_data.copy()
    product_variant_data2["sku"] = f"{new_product_data['sku']}-variant2"
    product_variant2 = await plytix.products.create_product(**product_variant_data2)

    result = await plytix.products.variants.link_variant_to_products(
        [(product.id, product_variant.id), (product2.id, product_variant2.id)]
    )

    assert result == [True, True]


async def test_link_variants_to_products_not_found(plytix):
    result = await plytix.products.variants.link_variant_to_products([("not_found", "not_found")])

    assert result == [False]
