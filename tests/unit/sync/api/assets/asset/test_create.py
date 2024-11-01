import pytest


def test_create_asset_from_url(plytix, new_asset_data_from_url_factory):
    asset = plytix.assets.create_asset_by_url(**new_asset_data_from_url_factory())

    assert asset.id is not None


def test_create_assets_from_urls(plytix, new_asset_data_from_url_factory):
    assets = plytix.assets.create_assets_by_urls([new_asset_data_from_url_factory(), new_asset_data_from_url_factory()])

    assert len(assets) == 2
    assert assets[0].id is not None
    assert assets[1].id is not None


@pytest.mark.skip("To be fixed in https://github.com/TheTelematic/plytix-pim-client/issues/26")
def test_create_asset_from_local_file(plytix, new_asset_data_from_local_file_factory):
    asset = plytix.assets.create_asset_from_local_file(**new_asset_data_from_local_file_factory())

    assert asset.id is not None


@pytest.mark.skip("To be fixed in https://github.com/TheTelematic/plytix-pim-client/issues/26")
def test_create_assets_from_local_files(plytix, new_asset_data_from_local_file_factory):
    assets = plytix.assets.create_assets_from_local_files([new_asset_data_from_local_file_factory()])

    assert len(assets) == 1
    assert assets[0].id is not None
