from plytix_pim_client.dtos.filters import AvailableSearchFilter


async def test_get_assets_filters(plytix_factory):
    filters = await plytix_factory.filters.get_assets_filters()

    assert isinstance(filters, list)
    assert all(isinstance(f, AvailableSearchFilter) for f in filters)


async def test_get_products_filters(plytix_factory):
    filters = await plytix_factory.filters.get_products_filters()

    assert isinstance(filters, list)
    assert all(isinstance(f, AvailableSearchFilter) for f in filters)


async def test_get_relationships_filters(plytix_factory):
    filters = await plytix_factory.filters.get_relationships_filters()

    assert isinstance(filters, list)
    assert all(isinstance(f, AvailableSearchFilter) for f in filters)
