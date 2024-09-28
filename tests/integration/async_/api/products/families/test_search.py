from plytix_pim_client.dtos.filters import OperatorEnum, SearchFilter
from plytix_pim_client.dtos.pagination import Pagination


async def test_search_families(plytix, new_product_family_data):
    new_family_data_1 = new_product_family_data.copy()
    new_family_data_2 = new_product_family_data.copy()
    new_family_data_3 = new_product_family_data.copy()

    new_family_data_1["name"] = f"{new_product_family_data['name']}-1"
    new_family_data_2["name"] = f"{new_product_family_data['name']}-2"
    new_family_data_3["name"] = f"{new_product_family_data['name']}-3"

    families = [
        new_family_data_1,
        new_family_data_2,
        new_family_data_3,
    ]
    await plytix.products.families.create_families(families)

    search_results = await plytix.products.families.search_families(
        filters=[[SearchFilter(field="name", operator=OperatorEnum.CONTAINS, value=new_product_family_data["name"])]],
        attributes=[
            "name",
        ],
        relationship_filters=[],
        pagination=Pagination(page=1, page_size=10, sort_by_attribute="name", sort_ascending=True),
    )

    assert len(search_results) == 3

    assert search_results[0].name == new_family_data_1["name"]
    assert search_results[1].name == new_family_data_2["name"]
    assert search_results[2].name == new_family_data_3["name"]


async def test_search_all_families(plytix, new_product_family_data):
    new_family_data_1 = new_product_family_data.copy()
    new_family_data_2 = new_product_family_data.copy()
    new_family_data_3 = new_product_family_data.copy()

    new_family_data_1["name"] = f"{new_product_family_data['name']}-1"
    new_family_data_2["name"] = f"{new_product_family_data['name']}-2"
    new_family_data_3["name"] = f"{new_product_family_data['name']}-3"

    families = [
        new_family_data_1,
        new_family_data_2,
        new_family_data_3,
    ]
    await plytix.products.families.create_families(families)

    search_results = []
    async for families in plytix.products.families.search_all_families(
        filters=[[SearchFilter(field="name", operator=OperatorEnum.CONTAINS, value=new_product_family_data["name"])]],
        attributes=["name", "label"],
        relationship_filters=[],
        sort_by_attribute="name",
        sort_ascending=True,
        page_size=2,
    ):
        search_results.extend(families)

    assert len(search_results) == 3

    assert search_results[0].name == new_family_data_1["name"]
    assert search_results[1].name == new_family_data_2["name"]
    assert search_results[2].name == new_family_data_3["name"]
