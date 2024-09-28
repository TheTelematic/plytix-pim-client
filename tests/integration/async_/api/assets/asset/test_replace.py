async def test_replace_asset(plytix, new_asset_data_from_url_factory, new_asset_data_from_local_file_factory):
    asset = await plytix.assets.create_asset_by_url(**new_asset_data_from_url_factory())
    old_modified_at = asset.modified

    result = await plytix.assets.replace_asset(asset.id, new_asset_data_from_local_file_factory()["file_path"])

    assert result.modified != old_modified_at


async def test_replace_asset_not_found(plytix, new_asset_data_from_local_file):
    result = await plytix.assets.replace_asset("non-existing-id", new_asset_data_from_local_file["file_path"])

    assert result is None


async def test_replace_multiple_assets(
      plytix, new_asset_data_from_url_factory, new_asset_data_from_local_file_factory):
    assets = await plytix.assets.create_assets_by_urls(
        [new_asset_data_from_url_factory(), new_asset_data_from_url_factory()]
    )
    asset_ids = [asset.id for asset in assets]

    results = await plytix.assets.replace_assets(
        [(asset_id, new_asset_data_from_local_file_factory()["file_path"]) for asset_id in asset_ids]
    )

    assert len(results) == 2
    assert results[0].modified != assets[0].modified
    assert results[1].modified != assets[1].modified
