from plytix_pim_client.dtos.filters import OperatorEnum, SearchFilter
from plytix_pim_client.dtos.pagination import Pagination


async def test_search_assets(plytix, new_asset_data_from_url_factory):
    new_asset_data_1 = new_asset_data_from_url_factory()
    new_asset_data_2 = new_asset_data_from_url_factory()
    new_asset_data_3 = new_asset_data_from_url_factory()
    assets = await plytix.assets.create_assets_by_urls(
        [
            new_asset_data_1,
            new_asset_data_2,
            new_asset_data_3,
        ]
    )

    search_results = await plytix.assets.search_assets(
        filters=[[SearchFilter(field="id", operator=OperatorEnum.IN, value=[asset.id for asset in assets])]],
        attributes=[
            "created",
        ],
        relationship_filters=[],
        pagination=Pagination(page=1, page_size=10, sort_by_attribute="created", sort_ascending=True),
    )

    assets_ids = list([asset.id for asset in sorted(assets, key=lambda asset: asset.created)])
    assert len(search_results) == 3
    assert search_results[0].id in assets_ids[0]
    assert search_results[1].id in assets_ids[1]
    assert search_results[2].id in assets_ids[2]


async def test_search_all_assets(plytix, new_asset_data_from_url_factory):
    new_asset_data_1 = new_asset_data_from_url_factory()
    new_asset_data_2 = new_asset_data_from_url_factory()
    new_asset_data_3 = new_asset_data_from_url_factory()
    assets = await plytix.assets.create_assets_by_urls(
        [
            new_asset_data_1,
            new_asset_data_2,
            new_asset_data_3,
        ]
    )

    search_results = []
    async for results in plytix.assets.search_all_assets(
        filters=[[SearchFilter(field="id", operator=OperatorEnum.IN, value=[asset.id for asset in assets])]],
        attributes=[
            "created",
        ],
        relationship_filters=[],
        sort_by_attribute="created",
        sort_ascending=True,
        page_size=2,
    ):
        search_results.extend(results)

    assets_ids = list([asset.id for asset in sorted(assets, key=lambda asset: asset.created)])
    assert len(search_results) == 3
    assert search_results[0].id in assets_ids[0]
    assert search_results[1].id in assets_ids[1]
    assert search_results[2].id in assets_ids[2]
