from plytix_pim_client.dtos.filters import OperatorEnum, RelationshipSearchFilter, SearchFilter
from plytix_pim_client.dtos.pagination import Pagination


async def test_search_products(plytix, new_product_data):
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
    await plytix.products.create_products(products)

    search_results = await plytix.products.search_products(
        filters=[[SearchFilter(field="sku", operator=OperatorEnum.CONTAINS, value=new_product_data["sku"])]],
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


async def test_search_all_products(plytix, new_product_data):
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
    await plytix.products.create_products(products)

    search_results = []
    async for products in plytix.products.search_all_products(
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


async def test_search_products_by_relationships(plytix, new_product_data, new_product_relationship_data):
    # Create product 1 (It won't be linked through the relationship)
    new_product_data_1 = new_product_data.copy()
    new_product_data_1["sku"] = f"{new_product_data['sku']}-1"
    await plytix.products.create_product(**new_product_data_1)

    # Create product 2 (it will be linked to product 3 through the relationship)
    new_product_data_2 = new_product_data.copy()
    new_product_data_2["sku"] = f"{new_product_data['sku']}-2"
    new_product_2 = await plytix.products.create_product(**new_product_data_2)

    # Create product 3 (it will be linked by product 2 through the relationship)
    new_product_data_3 = new_product_data.copy()
    new_product_data_3["sku"] = f"{new_product_data['sku']}-3"
    new_product_3 = await plytix.products.create_product(**new_product_data_3)

    # Create a product relationship
    relationship = new_product_relationship_data.copy()
    relationship["name"] = f"{relationship['name']}"

    product_relationship = await plytix.products.relationships.create_product_relationship(**relationship)

    # Link products 2 and 3 through the relationship
    await plytix.products.relationships.link_product_to_relationship(
        product_id=new_product_2.id,
        product_relationship_id=product_relationship.id,
        product_relationships=[
            {"product_id": new_product_3.id, "quantity": 7}
        ]
    )

    # Search for products by relationship
    search_results = await plytix.products.search_products(
        filters=[],
        attributes=["sku"],
        relationship_filters=[[
            RelationshipSearchFilter(
                relationship_id=product_relationship.id,
                operator=OperatorEnum.EXISTS,
                product_ids=[],
            )
        ]],
        pagination=Pagination(page=1, page_size=10, sort_by_attribute="sku", sort_ascending=True)
    )

    assert len(search_results) == 1
    assert search_results[0].sku == new_product_data_2["sku"]