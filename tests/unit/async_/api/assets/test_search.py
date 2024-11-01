from http import HTTPStatus

from plytix_pim_client.dtos.assets.asset import Asset
from plytix_pim_client.dtos.filters import OperatorEnum, SearchFilter
from plytix_pim_client.dtos.pagination import Pagination


async def test_search_assets(plytix_factory, response_factory, assert_requests_factory):
    asset1 = Asset(id="1", filename="asset1")
    asset2 = Asset(id="2", filename="asset2")
    asset3 = Asset(id="3", filename="asset3")
    plytix = plytix_factory(
        [
            response_factory(
                HTTPStatus.OK,
                [
                    {"id": asset1.id, "filename": asset1.filename},
                    {"id": asset2.id, "filename": asset2.filename},
                    {"id": asset3.id, "filename": asset3.filename},
                ],
            ),
        ]
    )

    search_results = await plytix_factory.assets.search_assets(
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


async def test_search_all_assets(plytix_factory, new_asset_data_from_url_factory):
    new_asset_data_1 = new_asset_data_from_url_factory()
    new_asset_data_2 = new_asset_data_from_url_factory()
    new_asset_data_3 = new_asset_data_from_url_factory()
    assets = await plytix_factory.assets.create_assets_by_urls(
        [
            new_asset_data_1,
            new_asset_data_2,
            new_asset_data_3,
        ]
    )

    search_results = []
    async for results in plytix_factory.assets.search_all_assets(
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
