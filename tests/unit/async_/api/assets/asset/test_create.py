from http import HTTPMethod, HTTPStatus

import pytest


async def test_create_asset_from_url(
    plytix_factory, response_factory, assert_requests_factory, new_asset_data_from_url_factory
):
    data = new_asset_data_from_url_factory()
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.OK, {"id": 1, "url": data["url"], "filename": data["filename"]}),
        ]
    )

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


async def test_create_assets_from_urls(
    plytix_factory, response_factory, assert_requests_factory, new_asset_data_from_url_factory
):
    data1 = new_asset_data_from_url_factory()
    data2 = new_asset_data_from_url_factory()
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.OK, {"id": 1, "url": data1["url"], "filename": data1["filename"]}),
            response_factory(HTTPStatus.OK, {"id": 2, "url": data2["url"], "filename": data2["filename"]}),
        ]
    )

    await plytix.assets.create_assets_by_urls([data1, data2])

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.POST,
                path="/api/v1/assets",
                json={
                    "url": data1["url"],
                    "filename": data1["filename"],
                },
            ),
            dict(
                method=HTTPMethod.POST,
                path="/api/v1/assets",
                json={
                    "url": data2["url"],
                    "filename": data2["filename"],
                },
            ),
        ]
    )


@pytest.mark.skip("To be fixed in https://github.com/TheTelematic/plytix-pim-client/issues/26")
async def test_create_asset_from_local_file(plytix_factory, new_asset_data_from_local_file_factory):
    assert False


@pytest.mark.skip("To be fixed in https://github.com/TheTelematic/plytix-pim-client/issues/26")
async def test_create_assets_from_local_files(plytix_factory, new_asset_data_from_local_file_factory):
    assert False
