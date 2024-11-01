from http import HTTPStatus, HTTPMethod

from plytix_pim_client.dtos.assets.asset import Asset


async def test_update_asset(plytix_factory, response_factory, assert_requests_factory, asset):
    new_filename = f"{asset.filename}-new"
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                {"id": asset.id, "url": asset.url, "filename": new_filename, "modified": f"{asset.modified}-new"},
            ),
        ]
    )

    result = await plytix.assets.update_asset(asset.id, new_filename)

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.PATCH,
                path=f"/api/v1/assets/{asset.id}",
                json={"filename": new_filename},
            )
        ]
    )
    assert result.filename == new_filename


async def test_update_asset_not_found(plytix_factory, response_factory, assert_requests_factory, asset):
    new_filename = f"{asset.filename}-new"
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.NOT_FOUND),
        ]
    )

    result = await plytix.assets.update_asset(asset.id, new_filename)

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.PATCH,
                path=f"/api/v1/assets/{asset.id}",
                json={"filename": new_filename},
            )
        ]
    )
    assert result is None


async def test_update_multiple_assets(plytix_factory, response_factory, assert_requests_factory):
    asset1 = Asset(id="1", url="http://example.test/1", filename="1.jpg", modified="1")
    asset2 = Asset(id="2", url="http://example.test/2", filename="2.jpg", modified="2")
    new_filename1 = f"{asset1.filename}-new"
    new_filename2 = f"{asset2.filename}-new"
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                {"id": asset1.id, "url": asset1.url, "filename": new_filename1, "modified": f"{asset1.modified}-new"},
            ),
            response_factory(
                HTTPStatus.OK,
                {"id": asset2.id, "url": asset2.url, "filename": new_filename2, "modified": f"{asset2.modified}-new"},
            ),
        ]
    )

    result = await plytix.assets.update_assets(
        [
            (asset1.id, {"filename": new_filename1}),
            (asset2.id, {"filename": new_filename2}),
        ]
    )

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.PATCH,
                path=f"/api/v1/assets/{asset1.id}",
                json={"filename": new_filename1},
            ),
            dict(
                method=HTTPMethod.PATCH,
                path=f"/api/v1/assets/{asset2.id}",
                json={"filename": new_filename2},
            ),
        ]
    )
    assert len(result) == 2
    assert result[0].filename == new_filename1
    assert result[1].filename == new_filename2
