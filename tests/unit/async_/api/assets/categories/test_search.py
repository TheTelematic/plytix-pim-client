from http import HTTPStatus, HTTPMethod

from plytix_pim_client.dtos.assets.category import AssetCategory
from plytix_pim_client.dtos.filters import OperatorEnum, SearchFilter
from plytix_pim_client.dtos.pagination import Pagination


async def test_search_asset_categories(plytix_factory, response_factory, assert_requests_factory):
    category1 = AssetCategory(id="1", name="category1")
    category2 = AssetCategory(id="2", name="category2")
    category3 = AssetCategory(id="3", name="category3")
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                [
                    {"id": category1.id, "name": category1.name},
                    {"id": category2.id, "name": category2.name},
                    {"id": category3.id, "name": category3.name},
                ],
            ),
        ]
    )

    search_results = await plytix.assets.categories.search_asset_categories(
        filters=[
            [SearchFilter(field="id", operator=OperatorEnum.IN, value=[category1.id, category2.id, category3.id])]
        ],
        attributes=[
            "modified",
        ],
        relationship_filters=[],
        pagination=Pagination(page=1, page_size=10, sort_by_attribute="modified", sort_ascending=True),
    )

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.POST,
                path="/api/v1/categories/file/search",
                json={
                    "filters": [
                        [
                            {
                                "field": "id",
                                "operator": OperatorEnum.IN,
                                "value": [category1.id, category2.id, category3.id],
                            }
                        ]
                    ],
                    "attributes": ["modified"],
                    "relationship_filters": [],
                    "pagination": {
                        "page": 1,
                        "page_size": 10,
                        "order": "modified",
                    },
                },
            ),
        ]
    )
    assert len(search_results) == 3
    assert search_results == [
        category1,
        category2,
        category3,
    ]


async def test_search_all_asset_categories(plytix_factory, response_factory, assert_requests_factory):
    category1 = AssetCategory(id="1", name="category1")
    category2 = AssetCategory(id="2", name="category2")
    category3 = AssetCategory(id="3", name="category3")
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                [
                    {"id": category1.id, "name": category1.name},
                    {"id": category2.id, "name": category2.name},
                ],
            ),
            response_factory(
                HTTPStatus.OK,
                [
                    {"id": category3.id, "name": category3.name},
                ],
            ),
            response_factory(
                HTTPStatus.OK,
                [],
            ),
        ]
    )

    search_results = []
    async for results in plytix.assets.categories.search_all_asset_categories(
        filters=[
            [SearchFilter(field="id", operator=OperatorEnum.IN, value=[category1.id, category2.id, category3.id])]
        ],
        attributes=[
            "modified",
        ],
        relationship_filters=[],
        sort_by_attribute="modified",
        sort_ascending=True,
        page_size=2,
    ):
        search_results.extend(results)

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.POST,
                path="/api/v1/categories/file/search",
                json={
                    "filters": [
                        [
                            {
                                "field": "id",
                                "operator": OperatorEnum.IN,
                                "value": [category1.id, category2.id, category3.id],
                            }
                        ]
                    ],
                    "attributes": ["modified"],
                    "relationship_filters": [],
                    "pagination": {
                        "page": 1,
                        "page_size": 2,
                        "order": "modified",
                    },
                },
            ),
            dict(
                method=HTTPMethod.POST,
                path="/api/v1/categories/file/search",
                json={
                    "filters": [
                        [
                            {
                                "field": "id",
                                "operator": OperatorEnum.IN,
                                "value": [category1.id, category2.id, category3.id],
                            }
                        ]
                    ],
                    "attributes": ["modified"],
                    "relationship_filters": [],
                    "pagination": {
                        "page": 2,
                        "page_size": 2,
                        "order": "modified",
                    },
                },
            ),
            dict(
                method=HTTPMethod.POST,
                path="/api/v1/categories/file/search",
                json={
                    "filters": [
                        [
                            {
                                "field": "id",
                                "operator": OperatorEnum.IN,
                                "value": [category1.id, category2.id, category3.id],
                            }
                        ]
                    ],
                    "attributes": ["modified"],
                    "relationship_filters": [],
                    "pagination": {
                        "page": 3,
                        "page_size": 2,
                        "order": "modified",
                    },
                },
            ),
        ]
    )
    assert len(search_results) == 3
    assert search_results == [
        category1,
        category2,
        category3,
    ]
