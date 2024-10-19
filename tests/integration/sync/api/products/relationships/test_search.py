from plytix_pim_client.dtos.filters import OperatorEnum, SearchFilter
from plytix_pim_client.dtos.pagination import Pagination


def test_search_product_relationships(plytix, new_product_relationship_data):
    new_product_data_1 = new_product_relationship_data.copy()
    new_product_data_2 = new_product_relationship_data.copy()
    new_product_data_3 = new_product_relationship_data.copy()
    new_product_data_1["name"] = f"{new_product_data_1['name']}-1"
    new_product_data_2["name"] = f"{new_product_data_2['name']}-2"
    new_product_data_3["name"] = f"{new_product_data_3['name']}-3"
    relationships = plytix.products.relationships.create_product_relationships(
        [new_product_data_1, new_product_data_2, new_product_data_3]
    )

    search_results = plytix.products.relationships.search_product_relationships(
        filters=[
            [
                SearchFilter(
                    field="id", operator=OperatorEnum.IN, value=[relationship.id for relationship in relationships]
                )
            ]
        ],
        attributes=[
            "name",
        ],
        relationship_filters=[],
        pagination=Pagination(page=1, page_size=10, sort_by_attribute="name", sort_ascending=True),
    )

    relationships_ids = list(
        [relationship.id for relationship in sorted(relationships, key=lambda relationship: relationship.name)]
    )
    assert len(search_results) == 3
    assert search_results[0].id in relationships_ids[0]
    assert search_results[1].id in relationships_ids[1]
    assert search_results[2].id in relationships_ids[2]


def test_search_all_product_relationships(plytix, new_product_relationship_data):
    new_product_data_1 = new_product_relationship_data.copy()
    new_product_data_2 = new_product_relationship_data.copy()
    new_product_data_3 = new_product_relationship_data.copy()
    new_product_data_1["name"] = f"{new_product_data_1['name']}-1"
    new_product_data_2["name"] = f"{new_product_data_2['name']}-2"
    new_product_data_3["name"] = f"{new_product_data_3['name']}-3"
    relationships = plytix.products.relationships.create_product_relationships(
        [new_product_data_1, new_product_data_2, new_product_data_3]
    )

    search_results = []
    for results in plytix.products.relationships.search_all_product_relationships(
        filters=[
            [
                SearchFilter(
                    field="id", operator=OperatorEnum.IN, value=[relationship.id for relationship in relationships]
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
        search_results.extend(results)

    relationships_ids = list(
        [relationship.id for relationship in sorted(relationships, key=lambda relationship: relationship.name)]
    )
    assert len(search_results) == 3
    assert search_results[0].id == relationships_ids[0]
    assert search_results[1].id == relationships_ids[1]
    assert search_results[2].id == relationships_ids[2]
