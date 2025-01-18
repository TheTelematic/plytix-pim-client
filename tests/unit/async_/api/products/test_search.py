from http import HTTPStatus, HTTPMethod

from plytix_pim_client.dtos.filters import OperatorEnum, SearchFilter
from plytix_pim_client.dtos.pagination import Pagination


async def test_search_products(plytix_factory, new_product_data, response_factory, assert_requests_factory):
    new_product_data_1 = new_product_data.copy()
    new_product_data_2 = new_product_data.copy()
    new_product_data_3 = new_product_data.copy()

    new_product_data_1["sku"] = f"{new_product_data['sku']}-1"
    new_product_data_2["sku"] = f"{new_product_data['sku']}-2"
    new_product_data_3["sku"] = f"{new_product_data['sku']}-3"
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                [
                    {"sku": new_product_data_1["sku"], "label": new_product_data_1["label"]},
                    {"sku": new_product_data_2["sku"], "label": new_product_data_2["label"]},
                    {"sku": new_product_data_3["sku"], "label": new_product_data_3["label"]},
                ],
            ),
        ]
    )

    search_results = await plytix.products.search_products(
        filters=[[SearchFilter(field="sku", operator=OperatorEnum.CONTAINS, value=new_product_data["sku"])]],
        attributes=["sku", "label"],
        relationship_filters=[],
        pagination=Pagination(page=1, page_size=10, sort_by_attribute="sku", sort_ascending=True),
    )

    assert assert_requests_factory(
        [
            dict(
                method=HTTPMethod.POST,
                path="/api/v1/products/search",
                json={
                    "filters": [
                        [
                            {
                                "field": "sku",
                                "operator": OperatorEnum.CONTAINS,
                                "value": new_product_data["sku"],
                            }
                        ]
                    ],
                    "attributes": ["sku", "label"],
                    "relationship_filters": [],
                    "pagination": {"order": "sku", "page": 1, "page_size": 10},
                },
            ),
        ]
    )
    assert len(search_results) == 3

    assert search_results[0].sku == new_product_data_1["sku"]
    assert search_results[0].label == new_product_data_1["label"]

    assert search_results[1].sku == new_product_data_2["sku"]
    assert search_results[1].label == new_product_data_2["label"]

    assert search_results[2].sku == new_product_data_3["sku"]
    assert search_results[2].label == new_product_data_3["label"]


async def test_search_all_products(plytix_factory, new_product_data):
    new_product_data_1 = new_product_data.copy()
    new_product_data_2 = new_product_data.copy()
    new_product_data_3 = new_product_data.copy()

    new_product_data_1["sku"] = f"{new_product_data['sku']}-1"
    new_product_data_2["sku"] = f"{new_product_data['sku']}-2"
    new_product_data_3["sku"] = f"{new_product_data['sku']}-3"

    products = [
        new_product_data_1,
        new_product_data_2,
        new_product_data_3,
    ]
    await plytix_factory.products.create_products(products)

    search_results = []
    async for products in plytix_factory.products.search_all_products(
        filters=[[SearchFilter(field="sku", operator=OperatorEnum.CONTAINS, value=new_product_data["sku"])]],
        attributes=["sku", "label"],
        relationship_filters=[],
        sort_by_attribute="sku",
        sort_ascending=True,
        page_size=2,
    ):
        search_results.extend(products)

    assert len(search_results) == 3

    assert search_results[0].sku == new_product_data_1["sku"]
    assert search_results[0].label == new_product_data_1["label"]

    assert search_results[1].sku == new_product_data_2["sku"]
    assert search_results[1].label == new_product_data_2["label"]

    assert search_results[2].sku == new_product_data_3["sku"]
    assert search_results[2].label == new_product_data_3["label"]
