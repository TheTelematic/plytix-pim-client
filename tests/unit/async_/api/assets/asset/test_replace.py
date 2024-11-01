import os
from http import HTTPStatus, HTTPMethod
from unittest.mock import ANY

from plytix_pim_client.dtos.assets.asset import Asset


async def test_replace_asset(
    plytix_factory, response_factory, assert_requests_factory, asset, new_asset_data_from_local_file_factory
):
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                {"id": asset.id, "url": asset.url, "filename": asset.filename, "modified": f"{asset.modified}-new"},
            ),
        ]
    )
    new_data = new_asset_data_from_local_file_factory()

    result = await plytix.assets.replace_asset(asset.id, new_data["file_path"])

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.PUT,
                path=f"/api/v1/assets/{asset.id}/content",
                files={"file": (os.path.basename(new_data["file_path"]), ANY)},
            )
        ]
    )
    assert result.modified != asset.modified


async def test_replace_asset_not_found(
    plytix_factory, response_factory, assert_requests_factory, new_asset_data_from_local_file_factory
):
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.NOT_FOUND),
        ]
    )
    asset_id = "non-existing-id"
    new_data = new_asset_data_from_local_file_factory()

    result = await plytix.assets.replace_asset(asset_id, new_data["file_path"])

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.PUT,
                path=f"/api/v1/assets/{asset_id}/content",
                files={"file": (os.path.basename(new_data["file_path"]), ANY)},
            )
        ]
    )
    assert result is None


async def test_replace_multiple_assets(
    plytix_factory, response_factory, assert_requests_factory, new_asset_data_from_local_file_factory
):
    asset1 = Asset(id="1", url="http://example.test/1", filename="1.jpg", modified="1")
    asset2 = Asset(id="2", url="http://example.test/2", filename="2.jpg", modified="2")
    new_data1 = new_asset_data_from_local_file_factory()
    new_data2 = new_asset_data_from_local_file_factory()
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                {"id": asset1.id, "url": asset1.url, "filename": asset1.filename, "modified": f"{asset1.modified}-new"},
            ),
            response_factory(
                HTTPStatus.OK,
                {"id": asset2.id, "url": asset2.url, "filename": asset2.filename, "modified": f"{asset2.modified}-new"},
            ),
        ]
    )

    results = await plytix.assets.replace_assets(
        [
            (asset1.id, new_data1["file_path"]),
            (asset2.id, new_data2["file_path"]),
        ]
    )

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.PUT,
                path=f"/api/v1/assets/{asset1.id}/content",
                files={"file": (os.path.basename(new_data1["file_path"]), ANY)},
            ),
            dict(
                method=HTTPMethod.PUT,
                path=f"/api/v1/assets/{asset2.id}/content",
                files={"file": (os.path.basename(new_data2["file_path"]), ANY)},
            ),
        ]
    )
    assert len(results) == 2
    assert results[0].modified != asset1.modified
    assert results[1].modified != asset2.modified
