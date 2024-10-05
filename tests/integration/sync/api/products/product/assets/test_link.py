def test_link_asset_to_product(plytix, product, asset, product_attribute_media):
    result = plytix.products.assets.link_asset_to_product(product.id, asset.id, product_attribute_media.label)

    assert result is True
    product = plytix.products.get_product(product.id)
    assert product.assets[0]["id"] == asset.id
    assert product.assets[0]["filename"] == asset.filename


def test_link_not_existing_product(plytix):
    result = plytix.products.assets.link_asset_to_product("not-existing", "not-existing", "not-existing")

    assert result is False


def test_link_multiple_asset_to_products(
    plytix, product, asset, product_attribute_media, new_product_data, new_asset_data_from_url_factory
):
    product2 = new_product_data.copy()
    product2["sku"] = f"{product2['sku']}-2"
    product2 = plytix.products.create_product(**product2)
    asset2 = plytix.assets.create_asset_by_url(**new_asset_data_from_url_factory())

    results = plytix.products.assets.link_asset_to_products(
        [
            (product.id, asset.id, product_attribute_media.label),
            (product2.id, asset2.id, product_attribute_media.label),
        ]
    )

    assert results == [True, True]
    product = plytix.products.get_product(product.id)
    product2 = plytix.products.get_product(product2.id)
    assert product.assets[0]["id"] == asset.id
    assert product2.assets[0]["id"] == asset2.id
    assert product.assets[0]["filename"] == asset.filename
    assert product2.assets[0]["filename"] == asset2.filename
