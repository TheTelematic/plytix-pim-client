from http import HTTPStatus, HTTPMethod

from plytix_pim_client.dtos.assets.asset import Asset


async def test_delete_asset(plytix_factory, response_factory, assert_requests_factory, asset):
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.NO_CONTENT,
            ),
        ]
    )

    result = await plytix.assets.delete_asset(asset.id)

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.DELETE,
                path=f"/api/v1/assets/{asset.id}",
            )
        ]
    )
    assert result is True


async def test_delete_asset_not_found(plytix_factory, response_factory, assert_requests_factory):
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.NOT_FOUND,
            ),
        ]
    )
    asset_id = "non-existing-id"

    result = await plytix.assets.delete_asset(asset_id)

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.DELETE,
                path=f"/api/v1/assets/{asset_id}",
            )
        ]
    )
    assert result is False


async def test_delete_multiple_assets(plytix_factory, response_factory, assert_requests_factory):
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.NO_CONTENT,
            ),
            response_factory(
                HTTPStatus.NO_CONTENT,
            ),
        ]
    )
    asset1 = Asset(id="1", url="http://example.test/1", filename="1.jpg")
    asset2 = Asset(id="2", url="http://example.test/2", filename="2.jpg")

    result = await plytix.assets.delete_assets([asset1.id, asset2.id])

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.DELETE,
                path=f"/api/v1/assets/{asset1.id}",
            ),
            dict(
                method=HTTPMethod.DELETE,
                path=f"/api/v1/assets/{asset2.id}",
            ),
        ]
    )
    assert result == [True, True]
