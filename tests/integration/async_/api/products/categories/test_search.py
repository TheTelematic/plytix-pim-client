import asyncio

from flaky import flaky  # type: ignore

from plytix_pim_client.dtos.filters import OperatorEnum, SearchFilter
from plytix_pim_client.dtos.pagination import Pagination


async def test_search_product_categories(plytix, new_product_category_data):
    new_product_data_1 = new_product_category_data.copy()
    new_product_data_2 = new_product_category_data.copy()
    new_product_data_3 = new_product_category_data.copy()
    new_product_data_1["name"] = f"{new_product_data_1['name']}-1"
    new_product_data_2["name"] = f"{new_product_data_2['name']}-2"
    new_product_data_3["name"] = f"{new_product_data_3['name']}-3"
    categories = await plytix.products.categories.create_product_categories(
        [new_product_data_1, new_product_data_2, new_product_data_3]
    )

    search_results = await plytix.products.categories.search_product_categories(
        filters=[[SearchFilter(field="id", operator=OperatorEnum.IN, value=[category.id for category in categories])]],
        attributes=[
            "modified",
        ],
        relationship_filters=[],
        pagination=Pagination(page=1, page_size=10, sort_by_attribute="modified", sort_ascending=True),
    )

    categories_ids = list([category.id for category in sorted(categories, key=lambda category: category.modified)])
    assert len(search_results) == 3
    assert search_results[0].id in categories_ids[0]
    assert search_results[1].id in categories_ids[1]
    assert search_results[2].id in categories_ids[2]


@flaky
async def test_search_all_product_categories(plytix, new_product_category_data):
    new_product_data_1 = new_product_category_data.copy()
    new_product_data_2 = new_product_category_data.copy()
    new_product_data_3 = new_product_category_data.copy()
    new_product_data_1["name"] = f"{new_product_data_1['name']}-1"
    new_product_data_2["name"] = f"{new_product_data_2['name']}-2"
    new_product_data_3["name"] = f"{new_product_data_3['name']}-3"
    categories = await plytix.products.categories.create_product_categories(
        [new_product_data_1, new_product_data_2, new_product_data_3]
    )

    await asyncio.sleep(3)
    search_results = []
    async for results in plytix.products.categories.search_all_product_categories(
        filters=[[SearchFilter(field="id", operator=OperatorEnum.IN, value=[category.id for category in categories])]],
        attributes=[
            "modified",
        ],
        relationship_filters=[],
        sort_by_attribute="modified",
        sort_ascending=True,
        page_size=2,
    ):
        search_results.extend(results)

    categories_ids = list([category.id for category in sorted(categories, key=lambda category: category.modified)])
    assert len(search_results) == 3
    assert search_results[0].id == categories_ids[0]
    assert search_results[1].id == categories_ids[1]
    assert search_results[2].id == categories_ids[2]
