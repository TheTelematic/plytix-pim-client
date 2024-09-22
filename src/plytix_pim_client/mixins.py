from plytix_pim_client.api.product_families.product_family.attributes.link import (
    LinkAttributeToFamilyAPISyncMixin,
    LinkAttributeToFamilyAPIAsyncMixin,
)
from plytix_pim_client.api.product_families.product_family.create import (
    FamilyCreateAPISyncMixin,
    FamilyCreateAPIAsyncMixin,
)
from plytix_pim_client.api.product_families.product_family.delete import (
    FamilyDeleteAPISyncMixin,
    FamilyDeleteAPIAsyncMixin,
)
from plytix_pim_client.api.product_families.product_family.get import FamilyGetAPISyncMixin, FamilyGetAPIAsyncMixin
from plytix_pim_client.api.product_families.product_family.update import (
    FamilyUpdateAPISyncMixin,
    FamilyUpdateAPIAsyncMixin,
)
from plytix_pim_client.api.product_families.search import FamiliesSearchAPISyncMixin, FamiliesSearchAPIAsyncMixin
from plytix_pim_client.api.products.attributes.attribute.create import (
    ProductAttributeCreateAPISyncMixin,
    ProductAttributeCreateAPIAsyncMixin,
)
from plytix_pim_client.api.products.product.create import ProductCreateAPISyncMixin, ProductCreateAPIAsyncMixin
from plytix_pim_client.api.products.product.delete import ProductDeleteAPISyncMixin, ProductDeleteAPIAsyncMixin
from plytix_pim_client.api.products.product.family import (
    ProductAssignFamilyAPISyncMixin,
    ProductAssignFamilyAPIAsyncMixin,
)
from plytix_pim_client.api.products.product.get import ProductGetAPISyncMixin, ProductGetAPIAsyncMixin
from plytix_pim_client.api.products.product.update import ProductUpdateAPISyncMixin, ProductUpdateAPIAsyncMixin
from plytix_pim_client.api.products.search import ProductsSearchAPISyncMixin, ProductsSearchAPIAsyncMixin


class _ProductsAPISync(
    ProductCreateAPISyncMixin,
    ProductsSearchAPISyncMixin,
    ProductGetAPISyncMixin,
    ProductUpdateAPISyncMixin,
    ProductDeleteAPISyncMixin,
    ProductAssignFamilyAPISyncMixin,
    ProductAttributeCreateAPISyncMixin,
): ...  # noqa: E701


class _ProductsAPIAsync(
    ProductCreateAPIAsyncMixin,
    ProductsSearchAPIAsyncMixin,
    ProductGetAPIAsyncMixin,
    ProductUpdateAPIAsyncMixin,
    ProductDeleteAPIAsyncMixin,
    ProductAssignFamilyAPIAsyncMixin,
    ProductAttributeCreateAPIAsyncMixin,
): ...  # noqa: E701


class _FamiliesAPISync(
    FamilyCreateAPISyncMixin,
    FamiliesSearchAPISyncMixin,
    FamilyGetAPISyncMixin,
    FamilyUpdateAPISyncMixin,
    FamilyDeleteAPISyncMixin,
    LinkAttributeToFamilyAPISyncMixin,
): ...  # noqa: E701


class _FamiliesAPIAsync(
    FamilyCreateAPIAsyncMixin,
    FamiliesSearchAPIAsyncMixin,
    FamilyGetAPIAsyncMixin,
    FamilyUpdateAPIAsyncMixin,
    FamilyDeleteAPIAsyncMixin,
    LinkAttributeToFamilyAPIAsyncMixin,
): ...  # noqa: E701
