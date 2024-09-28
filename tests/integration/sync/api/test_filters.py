from plytix_pim_client.dtos.filters import AvailableSearchFilter


def test_get_assets_filters(plytix):
    filters = plytix.filters.get_assets_filters()

    assert isinstance(filters, list)
    assert all(isinstance(f, AvailableSearchFilter) for f in filters)


def test_get_products_filters(plytix):
    filters = plytix.filters.get_products_filters()

    assert isinstance(filters, list)
    assert all(isinstance(f, AvailableSearchFilter) for f in filters)


def test_get_relationships_filters(plytix):
    filters = plytix.filters.get_relationships_filters()

    assert isinstance(filters, list)
    assert all(isinstance(f, AvailableSearchFilter) for f in filters)
