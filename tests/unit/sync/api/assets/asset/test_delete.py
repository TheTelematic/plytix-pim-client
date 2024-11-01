def test_delete_asset(plytix, new_asset_data_from_url_factory):
    asset = plytix.assets.create_asset_by_url(**new_asset_data_from_url_factory())

    result = plytix.assets.delete_asset(asset.id)

    assert result is True


def test_delete_asset_not_found(plytix):
    result = plytix.assets.delete_asset("non-existing-id")

    assert result is False


def test_delete_multiple_assets(plytix, new_asset_data_from_url_factory):
    assets = plytix.assets.create_assets_by_urls([new_asset_data_from_url_factory(), new_asset_data_from_url_factory()])
    asset_ids = [result.id for result in assets]

    results = plytix.assets.delete_assets(asset_ids)

    assert results[0] is True
    assert results[1] is True
