from http import HTTPStatus, HTTPMethod


async def test_create_asset_category(
    plytix_factory, response_factory, assert_requests_factory, new_asset_category_data
):
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.OK, {"id": 1, **new_asset_category_data}),
        ]
    )

    asset_category = await plytix.assets.categories.create_asset_category(**new_asset_category_data)

    assert assert_requests_factory(
        [dict(method=HTTPMethod.POST, path="/api/v1/categories/file", json=new_asset_category_data)]
    )
    assert asset_category.name == new_asset_category_data["name"]


async def test_create_asset_subcategory(
    plytix_factory, response_factory, assert_requests_factory, new_asset_category_data, asset_category
):
    subcategory_data = new_asset_category_data.copy()
    subcategory_data["name"] = f"{subcategory_data['name']}-sub"
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.OK, {"id": 1, "parents_ids": [asset_category.id], **subcategory_data}),
        ]
    )

    subcategory = await plytix.assets.categories.create_asset_category(
        **subcategory_data, parent_category_id=asset_category.id
    )

    assert assert_requests_factory(
        [dict(method=HTTPMethod.POST, path=f"/api/v1/categories/file/{asset_category.id}", json=subcategory_data)]
    )
    assert subcategory.name == subcategory_data["name"]
    assert subcategory.parents_ids == [asset_category.id]


async def test_create_asset_categories(
    plytix_factory, response_factory, assert_requests_factory, new_asset_category_data
):
    category1 = new_asset_category_data.copy()
    category2 = new_asset_category_data.copy()
    category1["name"] = f"{category1['name']}-1"
    category2["name"] = f"{category2['name']}-2"
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.OK, {"id": 1, **category1}),
            response_factory(HTTPStatus.OK, {"id": 2, **category2}),
        ]
    )

    asset_categories = await plytix.assets.categories.create_asset_categories([category1, category2])

    assert assert_requests_factory(
        [
            dict(method=HTTPMethod.POST, path="/api/v1/categories/file", json=category1),
            dict(method=HTTPMethod.POST, path="/api/v1/categories/file", json=category2),
        ]
    )
    assert asset_categories[0].name == category1["name"]
    assert asset_categories[1].name == category2["name"]


async def test_create_asset_subcategories(
    plytix_factory, response_factory, assert_requests_factory, new_asset_category_data, asset_category
):
    subcategory1_data = new_asset_category_data.copy()
    subcategory2_data = new_asset_category_data.copy()
    subcategory1_data["name"] = f"{subcategory1_data['name']}-sub1"
    subcategory2_data["name"] = f"{subcategory2_data['name']}-sub2"
    subcategory1_data["parent_category_id"] = asset_category.id
    subcategory2_data["parent_category_id"] = asset_category.id
    plytix = plytix_factory(
        [
            response_factory(HTTPStatus.OK, {"id": 1, "parents_ids": [asset_category.id], **subcategory1_data}),
            response_factory(HTTPStatus.OK, {"id": 2, "parents_ids": [asset_category.id], **subcategory2_data}),
        ]
    )

    subcategories = await plytix.assets.categories.create_asset_categories([subcategory1_data, subcategory2_data])

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.POST,
                path=f"/api/v1/categories/file/{asset_category.id}",
                json={"name": subcategory1_data["name"]},
            ),
            dict(
                method=HTTPMethod.POST,
                path=f"/api/v1/categories/file/{asset_category.id}",
                json={"name": subcategory2_data["name"]},
            ),
        ]
    )
    assert subcategories[0].name == subcategory1_data["name"]
    assert subcategories[0].parents_ids == [asset_category.id]
    assert subcategories[1].name == subcategory2_data["name"]
    assert subcategories[1].parents_ids == [asset_category.id]
