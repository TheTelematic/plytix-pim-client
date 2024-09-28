async def test_create_asset_from_url(plytix, new_asset_data_from_url_factory):
    asset = await plytix.assets.create_asset_by_url(**new_asset_data_from_url_factory())

    assert asset.id is not None


async def test_create_assets_from_urls(plytix, new_asset_data_from_url_factory):
    assets = await plytix.assets.create_assets_by_urls(
        [new_asset_data_from_url_factory(), new_asset_data_from_url_factory()]
    )

    assert len(assets) == 2
    assert assets[0].id is not None
    assert assets[1].id is not None


async def test_create_asset_from_local_file(plytix, new_asset_data_from_local_file):
    asset = await plytix.assets.create_asset_from_local_file(**new_asset_data_from_local_file)

    assert asset.id is not None


async def test_create_assets_from_local_files(plytix, new_asset_data_from_local_file):
    assets = await plytix.assets.create_assets_from_local_files([new_asset_data_from_local_file])

    assert len(assets) == 1
    assert assets[0].id is not None
