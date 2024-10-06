def test_unlink_variant_from_product(
    plytix,
    product,
    product_variant,
):
    result = plytix.products.variants.unlink_variant_from_product(product.id, product_variant.id)

    assert result is True


def test_unlink_variant_from_product_not_found(plytix):
    result = plytix.products.variants.unlink_variant_from_product("not_found", "not_found")

    assert result is False


def test_unlink_variants_to_products(plytix, product, product_variant, new_product_data):
    product2 = new_product_data.copy()
    product2["sku"] = f"{new_product_data['sku']}-2"
    product2 = plytix.products.create_product(**product2)
    product_variant_data2 = new_product_data.copy()
    product_variant_data2["sku"] = f"{new_product_data['sku']}-variant2"
    product_variant2 = plytix.products.create_product(**product_variant_data2)
    plytix.products.variants.link_variant_to_product(product2.id, product_variant2.id)

    result = plytix.products.variants.unlink_variant_from_products(
        [(product.id, product_variant.id), (product2.id, product_variant2.id)]
    )

    assert result == [True, True]


def test_unlink_variants_to_products_not_found(plytix):
    result = plytix.products.variants.unlink_variant_from_products([("not_found", "not_found")])

    assert result == [False]
