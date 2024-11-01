from http import HTTPStatus, HTTPMethod

from plytix_pim_client.dtos.assets.asset import Asset
from plytix_pim_client.dtos.filters import OperatorEnum, SearchFilter
from plytix_pim_client.dtos.pagination import Pagination


async def test_search_assets(plytix_factory, response_factory, assert_requests_factory):
    asset1 = Asset(id="1", filename="asset1")
    asset2 = Asset(id="2", filename="asset2")
    asset3 = Asset(id="3", filename="asset3")
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                [
                    {"id": asset1.id, "filename": asset1.filename},
                    {"id": asset2.id, "filename": asset2.filename},
                    {"id": asset3.id, "filename": asset3.filename},
                ],
            ),
        ]
    )

    search_results = await plytix.assets.search_assets(
        filters=[[SearchFilter(field="id", operator=OperatorEnum.IN, value=[asset1.id, asset2.id, asset3.id])]],
        attributes=[
            "created",
        ],
        relationship_filters=[],
        pagination=Pagination(page=1, page_size=10, sort_by_attribute="created", sort_ascending=True),
    )

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.POST,
                path="/api/v1/assets/search",
                json={
                    "filters": [
                        [
                            {
                                "field": "id",
                                "operator": OperatorEnum.IN,
                                "value": [asset1.id, asset2.id, asset3.id],
                            }
                        ]
                    ],
                    "attributes": ["created"],
                    "relationship_filters": [],
                    "pagination": {
                        "page": 1,
                        "page_size": 10,
                        "order": "created",
                    },
                },
            ),
        ]
    )
    assert len(search_results) == 3
    assert search_results == [
        asset1,
        asset2,
        asset3,
    ]


async def test_search_all_assets(plytix_factory, response_factory, assert_requests_factory):
    asset1 = Asset(id="1", filename="asset1")
    asset2 = Asset(id="2", filename="asset2")
    asset3 = Asset(id="3", filename="asset3")
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                [
                    {"id": asset1.id, "filename": asset1.filename},
                    {"id": asset2.id, "filename": asset2.filename},
                ],
            ),
            response_factory(
                HTTPStatus.OK,
                [
                    {"id": asset3.id, "filename": asset3.filename},
                ],
            ),
            response_factory(
                HTTPStatus.OK,
                [],
            ),
        ]
    )

    search_results = []
    async for results in plytix.assets.search_all_assets(
        filters=[[SearchFilter(field="id", operator=OperatorEnum.IN, value=[asset1.id, asset2.id, asset3.id])]],
        attributes=[
            "created",
        ],
        relationship_filters=[],
        sort_by_attribute="created",
        sort_ascending=True,
        page_size=2,
    ):
        search_results.extend(results)

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.POST,
                path="/api/v1/assets/search",
                json={
                    "filters": [
                        [
                            {
                                "field": "id",
                                "operator": OperatorEnum.IN,
                                "value": [asset1.id, asset2.id, asset3.id],
                            }
                        ]
                    ],
                    "attributes": ["created"],
                    "relationship_filters": [],
                    "pagination": {
                        "page": 1,
                        "page_size": 2,
                        "order": "created",
                    },
                },
            ),
            dict(
                method=HTTPMethod.POST,
                path="/api/v1/assets/search",
                json={
                    "filters": [
                        [
                            {
                                "field": "id",
                                "operator": OperatorEnum.IN,
                                "value": [asset1.id, asset2.id, asset3.id],
                            }
                        ]
                    ],
                    "attributes": ["created"],
                    "relationship_filters": [],
                    "pagination": {
                        "page": 2,
                        "page_size": 2,
                        "order": "created",
                    },
                },
            ),
            dict(
                method=HTTPMethod.POST,
                path="/api/v1/assets/search",
                json={
                    "filters": [
                        [
                            {
                                "field": "id",
                                "operator": OperatorEnum.IN,
                                "value": [asset1.id, asset2.id, asset3.id],
                            }
                        ]
                    ],
                    "attributes": ["created"],
                    "relationship_filters": [],
                    "pagination": {
                        "page": 3,
                        "page_size": 2,
                        "order": "created",
                    },
                },
            ),
        ]
    )
    assert len(search_results) == 3
    assert search_results == [
        asset1,
        asset2,
        asset3,
    ]
