from http import HTTPStatus, HTTPMethod

from plytix_pim_client.dtos.assets.asset import Asset


async def test_get_asset(plytix_factory, response_factory, assert_requests_factory, asset):
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.OK, {"id": asset.id, "url": asset.url, "filename": asset.filename}),
        ]
    )

    result = await plytix.assets.get_asset(asset.id)

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.GET,
                path=f"/api/v1/assets/{asset.id}",
            )
        ]
    )
    assert result.id == asset.id


async def test_get_asset_not_found(plytix_factory, response_factory, assert_requests_factory, asset):
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.NOT_FOUND),
        ]
    )
    asset_id = "non-existing-id"

    result = await plytix.assets.get_asset(asset_id)

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.GET,
                path=f"/api/v1/assets/{asset_id}",
            )
        ]
    )
    assert result is None


async def test_get_multiple_assets(plytix_factory, response_factory, assert_requests_factory):
    asset1 = Asset(id="1", url="http://example.test/1", filename="1.jpg")
    asset2 = Asset(id="2", url="http://example.test/2", filename="2.jpg")
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.OK, {"id": asset1.id, "url": asset1.url, "filename": asset1.filename}),
            response_factory(HTTPStatus.OK, {"id": asset2.id, "url": asset2.url, "filename": asset2.filename}),
        ]
    )

    results = await plytix.assets.get_assets([asset1.id, asset2.id])

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.GET,
                path=f"/api/v1/assets/{asset1.id}",
            ),
            dict(
                method=HTTPMethod.GET,
                path=f"/api/v1/assets/{asset2.id}",
            ),
        ]
    )
    assert len(results) == 2
    assert results[0].id == asset1.id
    assert results[1].id == asset2.id
