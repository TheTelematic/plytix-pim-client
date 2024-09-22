from plytix_pim_client.dtos.filters import SearchFilter, OperatorEnum
from plytix_pim_client.dtos.pagination import Pagination


def test_search_product_attributes(plytix, new_product_attribute_data):
    new_product_attribute_data_1 = new_product_attribute_data.copy()
    new_product_attribute_data_2 = new_product_attribute_data.copy()
    new_product_attribute_data_3 = new_product_attribute_data.copy()

    new_product_attribute_data_1["name"] = f"{new_product_attribute_data['name']}-1"
    new_product_attribute_data_2["name"] = f"{new_product_attribute_data['name']}-2"
    new_product_attribute_data_3["name"] = f"{new_product_attribute_data['name']}-3"

    product_attributes = [
        new_product_attribute_data_1,
        new_product_attribute_data_2,
        new_product_attribute_data_3,
    ]
    plytix.products.attributes.create_attributes(product_attributes)

    search_results = plytix.products.attributes.search_product_attributes(
        filters=[
            [SearchFilter(field="name", operator=OperatorEnum.CONTAINS, value=new_product_attribute_data["name"])]
        ],
        attributes=[
            "name",
        ],
        relationship_filters=[],
        pagination=Pagination(page=1, page_size=10, sort_by_attribute="name", sort_ascending=True),
    )

    assert len(search_results) == 3

    assert search_results[0].name == new_product_attribute_data_1["name"]
    assert search_results[1].name == new_product_attribute_data_2["name"]
    assert search_results[2].name == new_product_attribute_data_3["name"]


def test_search_all_product_attributes(plytix, new_product_attribute_data):
    new_product_attribute_data_1 = new_product_attribute_data.copy()
    new_product_attribute_data_2 = new_product_attribute_data.copy()
    new_product_attribute_data_3 = new_product_attribute_data.copy()

    new_product_attribute_data_1["name"] = f"{new_product_attribute_data['name']}-1"
    new_product_attribute_data_2["name"] = f"{new_product_attribute_data['name']}-2"
    new_product_attribute_data_3["name"] = f"{new_product_attribute_data['name']}-3"

    product_attributes = [
        new_product_attribute_data_1,
        new_product_attribute_data_2,
        new_product_attribute_data_3,
    ]
    plytix.products.attributes.create_attributes(product_attributes)

    search_results = []
    for product_attributes in plytix.products.attributes.search_all_product_attributes(
        filters=[
            [SearchFilter(field="name", operator=OperatorEnum.CONTAINS, value=new_product_attribute_data["name"])]
        ],
        attributes=[
            "name",
        ],
        relationship_filters=[],
        sort_by_attribute="name",
        sort_ascending=True,
        page_size=2,
    ):
        search_results.extend(product_attributes)

    assert len(search_results) == 3

    assert search_results[0].name == new_product_attribute_data_1["name"]
    assert search_results[1].name == new_product_attribute_data_2["name"]
    assert search_results[2].name == new_product_attribute_data_3["name"]
