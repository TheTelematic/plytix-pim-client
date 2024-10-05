async def test_get_one_asset(plytix, product, asset, product_attribute):
    await plytix.products.assets.link_asset_to_product(product.id, asset.id, product_attribute.label)

    assets = await plytix.products.assets.get_product_assets(product.id, asset.id)

    assert len(assets) == 1
    assert assets[0].id == asset.id
    assert assets[0].filename == asset.filename


async def test_get_one_asset_of_multiple_products(
    plytix, product, asset, new_product_data, new_asset_data_from_url_factory, product_attribute
):
    product2 = new_product_data.copy()
    product2["sku"] = f"{product2['sku']}-2"
    product2 = await plytix.products.create_product(**product2)
    asset2 = await plytix.assets.create_asset_by_url(**new_asset_data_from_url_factory())
    await plytix.products.assets.link_asset_to_products(
        [
            (product.id, asset.id, product_attribute.label),
            (product2.id, asset2.id, product_attribute.label),
        ]
    )

    assets_groups = await plytix.products.assets.get_multiple_product_assets(
        [
            (product.id, asset.id),
            (product2.id, asset2.id),
        ]
    )

    assert len(assets_groups) == 2
    assert len(assets_groups[0]) == 1
    assert len(assets_groups[1]) == 1
    assert assets_groups[0][0].id == asset.id
    assert assets_groups[0][0].filename == asset.filename
    assert assets_groups[1][0].id == asset2.id
    assert assets_groups[1][0].filename == asset2.filename


async def test_get_not_existing_asset(plytix):
    assets = await plytix.products.assets.get_product_assets("not-existing", "not-existing")

    assert assets is None


async def test_get_not_existing_asset_of_multiple_products(plytix):
    assets_groups = await plytix.products.assets.get_multiple_product_assets(
        [
            ("not-existing", "not-existing"),
            ("not-existing", "not-existing"),
        ]
    )

    assert assets_groups == [None, None]


async def test_get_all_assets_for_one_product(
    plytix, product, asset, new_asset_data_from_url_factory, product_attribute
):
    asset2 = await plytix.assets.create_asset_by_url(**new_asset_data_from_url_factory())
    await plytix.products.assets.link_asset_to_products(
        [
            (product.id, asset.id, product_attribute.label),
            (product.id, asset2.id, product_attribute.label),
        ]
    )

    assets = await plytix.products.assets.get_product_assets(product.id)

    assert len(assets) == 2
    assert assets[0].id == asset.id or asset2.id
    assert assets[0].filename == asset.filename or asset2.filename
    assert assets[1].id == asset.id or asset2.id
    assert assets[1].filename == asset.filename or asset2.filename


async def test_get_all_assets_for_multiple_products(
    plytix, product, asset, new_product_data, new_asset_data_from_url_factory, product_attribute
):
    product2 = new_product_data.copy()
    product2["sku"] = f"{product2['sku']}-2"
    product2 = await plytix.products.create_product(**product2)
    asset2 = await plytix.assets.create_asset_by_url(**new_asset_data_from_url_factory())
    await plytix.products.assets.link_asset_to_products(
        [
            (product.id, asset.id, product_attribute.label),
            (product.id, asset2.id, product_attribute.label),
            (product2.id, asset.id, product_attribute.label),
            (product2.id, asset2.id, product_attribute.label),
        ]
    )

    assets_groups = await plytix.products.assets.get_multiple_product_assets(
        [
            (product.id, None),
            (product2.id, None),
        ]
    )

    assert len(assets_groups) == 2
    assert len(assets_groups[0]) == 2
    assert len(assets_groups[1]) == 2
    assert assets_groups[0][0].id == asset.id or asset2.id
    assert assets_groups[0][0].filename == asset.filename or asset2.filename
    assert assets_groups[0][1].id == asset2.id or asset.id
    assert assets_groups[0][1].filename == asset2.filename or asset.filename
    assert assets_groups[1][0].id == asset.id or asset2.id
    assert assets_groups[1][0].filename == asset.filename or asset2.filename
    assert assets_groups[1][1].id == asset2.id or asset.id
    assert assets_groups[1][1].filename == asset2.filename or asset.filename
