from http import HTTPStatus, HTTPMethod

from plytix_pim_client.dtos.assets.category import AssetCategory


async def test_delete_asset_category(plytix_factory, response_factory, assert_requests_factory, asset_category):
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.NO_CONTENT),
        ]
    )

    result = await plytix.assets.categories.delete_asset_category(asset_category.id)

    assert assert_requests_factory(
        [dict(method=HTTPMethod.DELETE, path=f"/api/v1/categories/file/{asset_category.id}")]
    )
    assert result is True


async def test_delete_asset_category_with_non_existent_category(
    plytix_factory, response_factory, assert_requests_factory
):
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.NOT_FOUND),
        ]
    )
    asset_category_id = "non-existent-id"

    result = await plytix.assets.categories.delete_asset_category(asset_category_id)

    assert assert_requests_factory(
        [dict(method=HTTPMethod.DELETE, path=f"/api/v1/categories/file/{asset_category_id}")]
    )
    assert result is False


async def test_delete_asset_categories(
    plytix_factory, response_factory, assert_requests_factory, new_asset_category_data
):
    category1 = AssetCategory(id="1", **new_asset_category_data)
    category2 = AssetCategory(id="2", **new_asset_category_data)
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.NO_CONTENT),
            response_factory(HTTPStatus.NO_CONTENT),
        ]
    )

    result = await plytix.assets.categories.delete_asset_categories([category1.id, category2.id])

    assert assert_requests_factory(
        [
            dict(method=HTTPMethod.DELETE, path=f"/api/v1/categories/file/{category1.id}"),
            dict(method=HTTPMethod.DELETE, path=f"/api/v1/categories/file/{category2.id}"),
        ]
    )
    assert result == [True, True]
