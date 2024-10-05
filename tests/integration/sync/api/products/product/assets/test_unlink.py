def test_unlink_asset_from_product(plytix, product, asset, product_attribute_media):
    plytix.products.assets.link_asset_to_product(product.id, asset.id, product_attribute_media.label)

    result = plytix.products.assets.unlink_asset_from_product(product.id, asset.id)

    assert result is True
    product = plytix.products.get_product(product.id)
    assert product.assets == []


def test_unlink_not_existing_product(plytix):
    result = plytix.products.assets.unlink_asset_from_product("not-existing", "not-existing")

    assert result is False


def test_multiple_products_to_assets(
    plytix, product, asset, product_attribute_media, new_product_data, new_asset_data_from_url_factory
):
    product2 = new_product_data.copy()
    product2["sku"] = f"{product2['sku']}-2"
    product2 = plytix.products.create_product(**product2)
    asset2 = plytix.assets.create_asset_by_url(**new_asset_data_from_url_factory())
    plytix.products.assets.link_asset_to_products(
        [
            (product.id, asset.id, product_attribute_media.label),
            (product2.id, asset2.id, product_attribute_media.label),
        ]
    )

    results = plytix.products.assets.unlink_asset_from_products(
        [
            (product.id, asset.id),
            (product2.id, asset2.id),
        ]
    )

    assert results == [True, True]
    product = plytix.products.get_product(product.id)
    product2 = plytix.products.get_product(product2.id)
    assert product.assets == []
    assert product2.assets == []
