async def test_unlink_asset_from_product(plytix, product, asset, product_attribute_media):
    await plytix.products.assets.link_asset_to_product(product.id, asset.id, product_attribute_media.label)

    result = await plytix.products.assets.unlink_asset_from_product(product.id, asset.id)

    assert result is True
    product = await plytix.products.get_product(product.id)
    assert product.assets == []


async def test_unlink_not_existing_product(plytix):
    result = await plytix.products.assets.unlink_asset_from_product("not-existing", "not-existing")

    assert result is False


async def test_multiple_products_to_assets(
    plytix, product, asset, product_attribute_media, new_product_data, new_asset_data_from_url_factory
):
    product2 = new_product_data.copy()
    product2["sku"] = f"{product2['sku']}-2"
    product2 = await plytix.products.create_product(**product2)
    asset2 = await plytix.assets.create_asset_by_url(**new_asset_data_from_url_factory())
    await plytix.products.assets.link_asset_to_products(
        [
            (product.id, asset.id, product_attribute_media.label),
            (product2.id, asset2.id, product_attribute_media.label),
        ]
    )

    results = await plytix.products.assets.unlink_asset_from_products(
        [
            (product.id, asset.id),
            (product2.id, asset2.id),
        ]
    )

    assert results == [True, True]
    product = await plytix.products.get_product(product.id)
    product2 = await plytix.products.get_product(product2.id)
    assert product.assets == []
    assert product2.assets == []
