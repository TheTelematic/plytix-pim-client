from plytix_pim_client.api.assets.asset.create import AssetCreateAPIAsyncMixin, AssetCreateAPISyncMixin
from plytix_pim_client.api.assets.asset.delete import AssetDeleteAPIAsyncMixin, AssetDeleteAPISyncMixin
from plytix_pim_client.api.assets.asset.get import AssetGetAPIAsyncMixin, AssetGetAPISyncMixin
from plytix_pim_client.api.assets.asset.replace import AssetReplaceAPIAsyncMixin, AssetReplaceAPISyncMixin
from plytix_pim_client.api.assets.asset.update import AssetUpdateAPIAsyncMixin, AssetUpdateAPISyncMixin
from plytix_pim_client.api.assets.categories.category.create import (
    AssetCategoryCreateAPISyncMixin,
    AssetCategoryCreateAPIAsyncMixin,
)
from plytix_pim_client.api.assets.categories.category.delete import (
    AssetCategoryDeleteAPISyncMixin,
    AssetCategoryDeleteAPIAsyncMixin,
)
from plytix_pim_client.api.assets.categories.category.update import (
    AssetCategoryUpdateAPISyncMixin,
    AssetCategoryUpdateAPIAsyncMixin,
)
from plytix_pim_client.api.assets.categories.search import (
    AssetCategoriesSearchAPISyncMixin,
    AssetCategoriesSearchAPIAsyncMixin,
)
from plytix_pim_client.api.assets.search import AssetsSearchAPIAsyncMixin, AssetsSearchAPISyncMixin
from plytix_pim_client.api.filters import FiltersGetAPISyncMixin, FiltersGetAPIAsyncMixin
from plytix_pim_client.api.products.attributes.attribute.create import (
    ProductAttributeCreateAPIAsyncMixin,
    ProductAttributeCreateAPISyncMixin,
)
from plytix_pim_client.api.products.attributes.attribute.delete import (
    ProductAttributeDeleteAPIAsyncMixin,
    ProductAttributeDeleteAPISyncMixin,
)
from plytix_pim_client.api.products.attributes.attribute.get import (
    ProductAttributeGetAPIAsyncMixin,
    ProductAttributeGetAPISyncMixin,
)
from plytix_pim_client.api.products.attributes.attribute.update import (
    ProductAttributeUpdateAPIAsyncMixin,
    ProductAttributeUpdateAPISyncMixin,
)
from plytix_pim_client.api.products.attributes.search import (
    ProductAttributesSearchAPIAsyncMixin,
    ProductAttributesSearchAPISyncMixin,
)
from plytix_pim_client.api.products.families.family.attributes.get import (
    ProductFamilyGetAttributesAPIAsyncMixin,
    ProductFamilyGetAttributesAPISyncMixin,
)
from plytix_pim_client.api.products.families.family.attributes.inheritance import (
    ProductFamilyEditAttributeInheritanceAPIAsyncMixin,
    ProductFamilyEditAttributeInheritanceAPISyncMixin,
)
from plytix_pim_client.api.products.families.family.attributes.link import (
    ProductFamilyLinkAttributeAPIAsyncMixin,
    ProductFamilyLinkAttributeAPISyncMixin,
)
from plytix_pim_client.api.products.families.family.attributes.unlink import (
    ProductFamilyUnlinkAttributeAPIAsyncMixin,
    ProductFamilyUnlinkAttributeAPISyncMixin,
)
from plytix_pim_client.api.products.families.family.create import (
    ProductFamilyCreateAPIAsyncMixin,
    ProductFamilyCreateAPISyncMixin,
)
from plytix_pim_client.api.products.families.family.delete import (
    ProductFamilyDeleteAPIAsyncMixin,
    ProductFamilyDeleteAPISyncMixin,
)
from plytix_pim_client.api.products.families.family.get import (
    ProductFamilyGetAPIAsyncMixin,
    ProductFamilyGetAPISyncMixin,
)
from plytix_pim_client.api.products.families.family.update import (
    ProductFamilyUpdateAPIAsyncMixin,
    ProductFamilyUpdateAPISyncMixin,
)
from plytix_pim_client.api.products.families.search import (
    ProductFamiliesSearchAPIAsyncMixin,
    ProductFamiliesSearchAPISyncMixin,
)
from plytix_pim_client.api.products.product.create import ProductCreateAPIAsyncMixin, ProductCreateAPISyncMixin
from plytix_pim_client.api.products.product.delete import ProductDeleteAPIAsyncMixin, ProductDeleteAPISyncMixin
from plytix_pim_client.api.products.product.family import (
    ProductFamilyAssignAPIAsyncMixin,
    ProductFamilyAssignAPISyncMixin,
)
from plytix_pim_client.api.products.product.get import ProductGetAPIAsyncMixin, ProductGetAPISyncMixin
from plytix_pim_client.api.products.product.update import ProductUpdateAPIAsyncMixin, ProductUpdateAPISyncMixin
from plytix_pim_client.api.products.search import ProductsSearchAPIAsyncMixin, ProductsSearchAPISyncMixin


# Assets API
class _CategoriesAPISync(
    AssetCategoryCreateAPISyncMixin,
    AssetCategoryDeleteAPISyncMixin,
    AssetCategoryUpdateAPISyncMixin,
    AssetCategoriesSearchAPISyncMixin,
): ...  # noqa: E701


class _CategoriesAPIAsync(
    AssetCategoryCreateAPIAsyncMixin,
    AssetCategoryDeleteAPIAsyncMixin,
    AssetCategoryUpdateAPIAsyncMixin,
    AssetCategoriesSearchAPIAsyncMixin,
): ...  # noqa: E701


class _AssetsAPISync(
    AssetCreateAPISyncMixin,
    AssetDeleteAPISyncMixin,
    AssetGetAPISyncMixin,
    AssetUpdateAPISyncMixin,
    AssetReplaceAPISyncMixin,
    AssetsSearchAPISyncMixin,
):
    @property
    def categories(self) -> _CategoriesAPISync:
        return _CategoriesAPISync(self._client)


class _AssetsAPIAsync(
    AssetCreateAPIAsyncMixin,
    AssetDeleteAPIAsyncMixin,
    AssetGetAPIAsyncMixin,
    AssetUpdateAPIAsyncMixin,
    AssetReplaceAPIAsyncMixin,
    AssetsSearchAPIAsyncMixin,
):
    @property
    def categories(self) -> _CategoriesAPIAsync:
        return _CategoriesAPIAsync(self._client)


# Filters API
class _FiltersAPISync(
    FiltersGetAPISyncMixin,
): ...  # noqa: E701


class _FiltersAPIAsync(
    FiltersGetAPIAsyncMixin,
): ...  # noqa: E701


# Product Families Attributes API
class _ProductFamiliesAttributesAPISync(
    ProductFamilyGetAttributesAPISyncMixin,
    ProductFamilyLinkAttributeAPISyncMixin,
    ProductFamilyEditAttributeInheritanceAPISyncMixin,
    ProductFamilyUnlinkAttributeAPISyncMixin,
): ...  # noqa: E701


class _ProductFamiliesAttributesAPIAsync(
    ProductFamilyGetAttributesAPIAsyncMixin,
    ProductFamilyLinkAttributeAPIAsyncMixin,
    ProductFamilyEditAttributeInheritanceAPIAsyncMixin,
    ProductFamilyUnlinkAttributeAPIAsyncMixin,
): ...  # noqa: E701


# Product Families API
class _ProductFamiliesAPISync(
    ProductFamilyCreateAPISyncMixin,
    ProductFamiliesSearchAPISyncMixin,
    ProductFamilyGetAPISyncMixin,
    ProductFamilyUpdateAPISyncMixin,
    ProductFamilyDeleteAPISyncMixin,
):
    @property
    def attributes(self) -> _ProductFamiliesAttributesAPISync:
        return _ProductFamiliesAttributesAPISync(self._client)


class _FamiliesAPIAsync(
    ProductFamilyCreateAPIAsyncMixin,
    ProductFamiliesSearchAPIAsyncMixin,
    ProductFamilyGetAPIAsyncMixin,
    ProductFamilyUpdateAPIAsyncMixin,
    ProductFamilyDeleteAPIAsyncMixin,
):
    @property
    def attributes(self) -> _ProductFamiliesAttributesAPIAsync:
        return _ProductFamiliesAttributesAPIAsync(self._client)


# Product Attributes API
class _ProductAttributesAPISync(
    ProductAttributeCreateAPISyncMixin,
    ProductAttributeDeleteAPISyncMixin,
    ProductAttributeGetAPISyncMixin,
    ProductAttributeUpdateAPISyncMixin,
    ProductAttributesSearchAPISyncMixin,
): ...  # noqa: E701


class _ProductAttributesAPIAsync(
    ProductAttributeCreateAPIAsyncMixin,
    ProductAttributeDeleteAPIAsyncMixin,
    ProductAttributeGetAPIAsyncMixin,
    ProductAttributeUpdateAPIAsyncMixin,
    ProductAttributesSearchAPIAsyncMixin,
): ...  # noqa: E701


# Products API
class _ProductsAPISync(
    ProductCreateAPISyncMixin,
    ProductsSearchAPISyncMixin,
    ProductGetAPISyncMixin,
    ProductUpdateAPISyncMixin,
    ProductDeleteAPISyncMixin,
    ProductFamilyAssignAPISyncMixin,
):
    @property
    def attributes(self) -> _ProductAttributesAPISync:
        return _ProductAttributesAPISync(self._client)

    @property
    def families(self) -> _ProductFamiliesAPISync:
        return _ProductFamiliesAPISync(self._client)


class _ProductsAPIAsync(
    ProductCreateAPIAsyncMixin,
    ProductsSearchAPIAsyncMixin,
    ProductGetAPIAsyncMixin,
    ProductUpdateAPIAsyncMixin,
    ProductDeleteAPIAsyncMixin,
    ProductFamilyAssignAPIAsyncMixin,
):
    @property
    def attributes(self) -> _ProductAttributesAPIAsync:
        return _ProductAttributesAPIAsync(self._client)

    @property
    def families(self) -> _FamiliesAPIAsync:
        return _FamiliesAPIAsync(self._client)
