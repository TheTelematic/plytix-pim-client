from http import HTTPStatus, HTTPMethod

from plytix_pim_client.dtos.filters import AvailableSearchFilter


async def test_get_assets_filters(plytix_factory, response_factory, assert_requests_factory):
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                [
                    {
                        "attributes": [
                            {
                                "filter_type": "filter_type",
                                "key": "key",
                                "operators": ["operator1", "operator2"],
                                "options": ["option1"],
                            }
                        ],
                        "properties": [
                            {
                                "filter_type": "filter_type",
                                "key": "key",
                                "operators": ["operator1"],
                            }
                        ],
                    }
                ],
            ),
        ]
    )

    filters = await plytix.filters.get_assets_filters()

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.GET,
                path="/api/v1/filters/asset",
            ),
        ]
    )
    assert isinstance(filters, list)
    assert all(isinstance(f, AvailableSearchFilter) for f in filters)


async def test_get_products_filters(plytix_factory, response_factory, assert_requests_factory):
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                [
                    {
                        "attributes": [
                            {
                                "filter_type": "filter_type",
                                "key": "key",
                                "operators": ["operator1", "operator2"],
                                "options": ["option1"],
                            }
                        ],
                        "properties": [
                            {
                                "filter_type": "filter_type",
                                "key": "key",
                                "operators": ["operator1"],
                            }
                        ],
                    }
                ],
            ),
        ]
    )

    filters = await plytix.filters.get_products_filters()

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.GET,
                path="/api/v1/filters/product",
            ),
        ]
    )
    assert isinstance(filters, list)
    assert all(isinstance(f, AvailableSearchFilter) for f in filters)


async def test_get_relationships_filters(plytix_factory, response_factory, assert_requests_factory):
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                [
                    {
                        "attributes": [
                            {
                                "filter_type": "filter_type",
                                "key": "key",
                                "operators": ["operator1", "operator2"],
                                "options": ["option1"],
                            }
                        ],
                        "properties": [
                            {
                                "filter_type": "filter_type",
                                "key": "key",
                                "operators": ["operator1"],
                            }
                        ],
                    }
                ],
            ),
        ]
    )

    filters = await plytix.filters.get_relationships_filters()

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.GET,
                path="/api/v1/filters/relationships",
            ),
        ]
    )
    assert isinstance(filters, list)
    assert all(isinstance(f, AvailableSearchFilter) for f in filters)
