from http import HTTPMethod, HTTPStatus

import pytest


async def test_create_asset_from_url(
    plytix_factory, response_factory, assert_requests_factory, new_asset_data_from_url_factory
):
    plytix = plytix_factory([response_factory(HTTPStatus.OK, {"id": 1, "url": "http://example.test/image.jpg"})])
    data = new_asset_data_from_url_factory()

    await plytix.assets.create_asset_by_url(**data)

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.POST,
                path="/api/v1/assets",
                json={
                    "url": data["url"],
                    "filename": data["filename"],
                },
            )
        ]
    )


async def test_create_assets_from_urls(plytix_factory, new_asset_data_from_url_factory):
    assets = await plytix_factory.assets.create_assets_by_urls(
        [new_asset_data_from_url_factory(), new_asset_data_from_url_factory()]
    )

    assert len(assets) == 2
    assert assets[0].id is not None
    assert assets[1].id is not None


@pytest.mark.skip("To be fixed in https://github.com/TheTelematic/plytix-pim-client/issues/26")
async def test_create_asset_from_local_file(plytix_factory, new_asset_data_from_local_file_factory):
    asset = await plytix_factory.assets.create_asset_from_local_file(**new_asset_data_from_local_file_factory())

    assert asset.id is not None


@pytest.mark.skip("To be fixed in https://github.com/TheTelematic/plytix-pim-client/issues/26")
async def test_create_assets_from_local_files(plytix_factory, new_asset_data_from_local_file_factory):
    assets = await plytix_factory.assets.create_assets_from_local_files([new_asset_data_from_local_file_factory()])

    assert len(assets) == 1
    assert assets[0].id is not None
