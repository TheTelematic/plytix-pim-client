from http import HTTPStatus, HTTPMethod

from plytix_pim_client.dtos.assets.category import AssetCategory


async def test_convert_to_first_level_category(
    plytix_factory, response_factory, assert_requests_factory, asset_category, asset_subcategory
):
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.OK, {"id": asset_subcategory.id, "parents_ids": []}),
        ]
    )

    subcategory = await plytix.assets.categories.convert_to_first_level_category(asset_subcategory.id)

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.PATCH, path=f"/api/v1/categories/file/{asset_subcategory.id}", json={"parent_id": ""}
            ),
        ]
    )
    assert subcategory.parents_ids == []


async def test_move_category(
    plytix_factory,
    response_factory,
    assert_requests_factory,
    asset_category,
    asset_subcategory,
    new_asset_category_data,
):
    new_parent_category = AssetCategory(id="3", **new_asset_category_data)
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.OK, {"id": asset_subcategory.id, "parents_ids": [new_parent_category.id]}),
        ]
    )

    subcategory = await plytix.assets.categories.move_category(asset_subcategory.id, new_parent_category.id)

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.PATCH,
                path=f"/api/v1/categories/file/{asset_subcategory.id}",
                json={"parent_id": new_parent_category.id},
            ),
        ]
    )
    assert subcategory.parents_ids == [new_parent_category.id]


async def test_sorting_category(
    plytix_factory,
    response_factory,
    assert_requests_factory,
    asset_category,
    asset_subcategory,
    new_asset_category_data,
):
    asset_subcategory2 = new_asset_category_data.copy()
    asset_subcategory2["name"] = f"{asset_subcategory2['name']}-sub2"
    asset_subcategory2 = AssetCategory(id="3", **asset_subcategory2)
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.OK, json={"id": asset_category.id, "n_children": "2"}),
        ]
    )

    await plytix.assets.categories.sorting_category(asset_category.id, [asset_subcategory2.id, asset_subcategory.id])

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.PATCH,
                path=f"/api/v1/categories/file/{asset_category.id}",
                json={"sort_children": [asset_subcategory2.id, asset_subcategory.id]},
            )
        ]
    )


async def test_sorting_root_category(
    plytix_factory, response_factory, assert_requests_factory, asset_category, new_asset_category_data
):
    asset_category2 = new_asset_category_data.copy()
    asset_category2["name"] = f"{asset_category2['name']}-sub2"
    asset_category2 = AssetCategory(id="2", **asset_category2)
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.OK, json={"id": asset_category.id, "n_children": "2"}),
        ]
    )

    await plytix.assets.categories.sorting_root_category([asset_category2.id, asset_category.id])

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.PATCH,
                path="/api/v1/categories/file/root",
                json={"sort_children": [asset_category2.id, asset_category.id]},
            )
        ]
    )


async def test_convert_to_first_level_multiple_categories(
    plytix_factory, response_factory, assert_requests_factory, asset_category, new_asset_category_data
):
    subcategory1 = AssetCategory(id="2", **new_asset_category_data)
    subcategory2 = AssetCategory(id="3", **new_asset_category_data)
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.OK, {"id": subcategory1.id, "parents_ids": []}),
            response_factory(HTTPStatus.OK, {"id": subcategory2.id, "parents_ids": []}),
        ]
    )

    subcategories = await plytix.assets.categories.convert_to_first_level_categories([subcategory1.id, subcategory2.id])

    assert assert_requests_factory(
        [
            dict(method=HTTPMethod.PATCH, path=f"/api/v1/categories/file/{subcategory1.id}", json={"parent_id": ""}),
            dict(method=HTTPMethod.PATCH, path=f"/api/v1/categories/file/{subcategory2.id}", json={"parent_id": ""}),
        ]
    )
    assert subcategories[0].parents_ids == []
    assert subcategories[1].parents_ids == []


async def test_move_multiple_categories(
    plytix_factory,
    response_factory,
    assert_requests_factory,
    asset_category,
    asset_subcategory,
    new_asset_category_data,
):
    subcategory1 = AssetCategory(id="3", **new_asset_category_data)
    subcategory2 = AssetCategory(id="4", **new_asset_category_data)
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.OK, {"id": asset_subcategory.id, "parents_ids": [asset_category.id]}),
            response_factory(HTTPStatus.OK, {"id": asset_subcategory.id, "parents_ids": [asset_category.id]}),
        ]
    )

    subcategories = await plytix.assets.categories.move_categories(
        [(subcategory1.id, asset_category.id), (subcategory2.id, asset_category.id)],
    )

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.PATCH,
                path=f"/api/v1/categories/file/{subcategory1.id}",
                json={"parent_id": asset_category.id},
            ),
            dict(
                method=HTTPMethod.PATCH,
                path=f"/api/v1/categories/file/{subcategory2.id}",
                json={"parent_id": asset_category.id},
            ),
        ]
    )
    assert subcategories[0].parents_ids == [asset_category.id]
    assert subcategories[1].parents_ids == [asset_category.id]
