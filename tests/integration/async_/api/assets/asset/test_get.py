async def test_get_asset(plytix, new_asset_data_from_url_factory):
    asset = await plytix.assets.create_asset_by_url(**new_asset_data_from_url_factory())

    result = await plytix.assets.get_asset(asset.id)

    assert result.id == asset.id


async def test_get_asset_not_found(plytix):
    result = await plytix.assets.get_asset("non-existing-id")

    assert result is None


async def test_get_multiple_assets(plytix, new_asset_data_from_url_factory):
    assets = await plytix.assets.create_assets_by_urls(
        [new_asset_data_from_url_factory(), new_asset_data_from_url_factory()]
    )

    asset_ids = [result.id for result in assets]
    results = await plytix.assets.get_assets(asset_ids)

    assert len(results) == 2
    assert results[0].id == assets[0].id
    assert results[1].id == assets[1].id
