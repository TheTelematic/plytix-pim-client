async def test_update_asset(plytix, new_asset_data_from_url_factory):
    asset = await plytix.assets.create_asset_by_url(**new_asset_data_from_url_factory())
    new_filename = f"{asset.filename.split('.')[0]}-new.{asset.filename.split('.')[1]}"

    result = await plytix.assets.update_asset(asset.id, new_filename)

    assert result.filename == new_filename


async def test_update_asset_not_found(plytix):
    result = await plytix.assets.update_asset("non-existing-id", "new-filename")

    assert result is None


async def test_update_multiple_assets(plytix, new_asset_data_from_url_factory):
    assets = await plytix.assets.create_assets_by_urls(
        [new_asset_data_from_url_factory(), new_asset_data_from_url_factory()]
    )

    updated_assets = [
        (asset.id, {"filename": f"{asset.filename.split('.')[0]}-new.{asset.filename.split('.')[1]}"})
        for asset in assets
    ]
    results = await plytix.assets.update_assets(updated_assets)

    assert len(results) == 2
    assert results[0].filename == updated_assets[0][1]["filename"]
    assert results[1].filename == updated_assets[1][1]["filename"]
