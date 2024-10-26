from plytix_pim_client.dtos.filters import OperatorEnum, SearchFilter
from plytix_pim_client.dtos.pagination import Pagination


def test_search_product_attributes_groups(plytix, new_product_attributes_group_data):
    new_product_attributes_group_data_1 = new_product_attributes_group_data.copy()
    new_product_attributes_group_data_2 = new_product_attributes_group_data.copy()
    new_product_attributes_group_data_3 = new_product_attributes_group_data.copy()

    new_product_attributes_group_data_1["name"] = f"{new_product_attributes_group_data['name']}-1"
    new_product_attributes_group_data_2["name"] = f"{new_product_attributes_group_data['name']}-2"
    new_product_attributes_group_data_3["name"] = f"{new_product_attributes_group_data['name']}-3"

    product_attributes_groups = [
        new_product_attributes_group_data_1,
        new_product_attributes_group_data_2,
        new_product_attributes_group_data_3,
    ]
    plytix.products.attributes.groups.create_attributes_groups(product_attributes_groups)

    search_results = plytix.products.attributes.groups.search_product_attributes_groups(
        filters=[
            [
                SearchFilter(
                    field="name", operator=OperatorEnum.CONTAINS, value=new_product_attributes_group_data["name"]
                )
            ]
        ],
        attributes=[
            "name",
        ],
        relationship_filters=[],
        pagination=Pagination(page=1, page_size=10, sort_by_attribute="name", sort_ascending=True),
    )

    assert len(search_results) == 3

    assert search_results[0].name == new_product_attributes_group_data_1["name"]
    assert search_results[1].name == new_product_attributes_group_data_2["name"]
    assert search_results[2].name == new_product_attributes_group_data_3["name"]


def test_search_all_product_attributes_groups(plytix, new_product_attributes_group_data):
    new_product_attributes_group_data_1 = new_product_attributes_group_data.copy()
    new_product_attributes_group_data_2 = new_product_attributes_group_data.copy()
    new_product_attributes_group_data_3 = new_product_attributes_group_data.copy()

    new_product_attributes_group_data_1["name"] = f"{new_product_attributes_group_data['name']}-1"
    new_product_attributes_group_data_2["name"] = f"{new_product_attributes_group_data['name']}-2"
    new_product_attributes_group_data_3["name"] = f"{new_product_attributes_group_data['name']}-3"

    product_attributes_groups = [
        new_product_attributes_group_data_1,
        new_product_attributes_group_data_2,
        new_product_attributes_group_data_3,
    ]
    plytix.products.attributes.groups.create_attributes_groups(product_attributes_groups)

    search_results = []
    for product_attributes_groups in plytix.products.attributes.groups.search_all_product_attributes_groups(
        filters=[
            [
                SearchFilter(
                    field="name", operator=OperatorEnum.CONTAINS, value=new_product_attributes_group_data["name"]
                )
            ]
        ],
        attributes=[
            "name",
        ],
        relationship_filters=[],
        sort_by_attribute="name",
        sort_ascending=True,
        page_size=2,
    ):
        search_results.extend(product_attributes_groups)

    assert len(search_results) == 3

    assert search_results[0].name == new_product_attributes_group_data_1["name"]
    assert search_results[1].name == new_product_attributes_group_data_2["name"]
    assert search_results[2].name == new_product_attributes_group_data_3["name"]
