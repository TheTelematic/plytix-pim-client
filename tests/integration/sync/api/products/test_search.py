from plytix_pim_client.dtos.filters import ProductsSearchFilter, OperatorEnum
from plytix_pim_client.dtos.pagination import Pagination


def test_search_products(client, new_product_data):
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
    client.products.create_products(products)

    search_results = client.products.search_products(
        filters=[[ProductsSearchFilter(field="sku", operator=OperatorEnum.CONTAINS, value=new_product_data["sku"])]],
        attributes=["sku", "label"],
        relationship_filters=[],
        pagination=Pagination(page=1, page_size=10, sort_by_attribute="sku", sort_ascending=True),
    )

    assert len(search_results) == 3

    assert search_results[0].sku == new_product_data_1["sku"]
    assert search_results[0].label == new_product_data_1["label"]

    assert search_results[1].sku == new_product_data_2["sku"]
    assert search_results[1].label == new_product_data_2["label"]

    assert search_results[2].sku == new_product_data_3["sku"]
    assert search_results[2].label == new_product_data_3["label"]
