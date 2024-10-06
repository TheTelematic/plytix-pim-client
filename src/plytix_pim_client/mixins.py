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
from plytix_pim_client.api.products.categories.category.create import (
    ProductCategoryCreateAPISyncMixin,
    ProductCategoryCreateAPIAsyncMixin,
)
from plytix_pim_client.api.products.categories.category.delete import (
    ProductCategoryDeleteAPISyncMixin,
    ProductCategoryDeleteAPIAsyncMixin,
)
from plytix_pim_client.api.products.categories.category.update import (
    ProductCategoryUpdateAPISyncMixin,
    ProductCategoryUpdateAPIAsyncMixin,
)
from plytix_pim_client.api.products.categories.search import (
    ProductCategoriesSearchAPISyncMixin,
    ProductCategoriesSearchAPIAsyncMixin,
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
from plytix_pim_client.api.products.product.assets.get import (
    ProductAssetsGetAPISyncMixin,
    ProductAssetsGetAPIAsyncMixin,
)
from plytix_pim_client.api.products.product.assets.link import (
    ProductAssetLinkAPISyncMixin,
    ProductAssetLinkAPIAsyncMixin,
)
from plytix_pim_client.api.products.product.assets.unlink import (
    ProductAssetUnlinkAPISyncMixin,
    ProductAssetUnlinkAPIAsyncMixin,
)
from plytix_pim_client.api.products.product.categories.get import (
    ProductCategoriesGetAPISyncMixin,
    ProductCategoriesGetAPIAsyncMixin,
)
from plytix_pim_client.api.products.product.categories.link import (
    ProductCategoryLinkAPISyncMixin,
    ProductCategoryLinkAPIAsyncMixin,
)
from plytix_pim_client.api.products.product.categories.unlink import (
    ProductCategoryUnlinkAPISyncMixin,
    ProductCategoryUnlinkAPIAsyncMixin,
)
from plytix_pim_client.api.products.product.create import ProductCreateAPIAsyncMixin, ProductCreateAPISyncMixin
from plytix_pim_client.api.products.product.delete import ProductDeleteAPIAsyncMixin, ProductDeleteAPISyncMixin
from plytix_pim_client.api.products.product.family import (
    ProductFamilyAssignAPIAsyncMixin,
    ProductFamilyAssignAPISyncMixin,
)
from plytix_pim_client.api.products.product.get import ProductGetAPIAsyncMixin, ProductGetAPISyncMixin
from plytix_pim_client.api.products.product.update import ProductUpdateAPIAsyncMixin, ProductUpdateAPISyncMixin
from plytix_pim_client.api.products.product.variants.get import (
    ProductVariantsGetAPISyncMixin,
    ProductVariantsGetAPIAsyncMixin,
)
from plytix_pim_client.api.products.product.variants.link import (
    ProductVariantLinkAPISyncMixin,
    ProductVariantLinkAPIAsyncMixin,
)
from plytix_pim_client.api.products.search import ProductsSearchAPIAsyncMixin, ProductsSearchAPISyncMixin


# Assets API
class _AssetCategoriesAPISync(
    AssetCategoryCreateAPISyncMixin,
    AssetCategoryDeleteAPISyncMixin,
    AssetCategoryUpdateAPISyncMixin,
    AssetCategoriesSearchAPISyncMixin,
): ...  # noqa: E701


class _AssetCategoriesAPIAsync(
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
    def categories(self) -> _AssetCategoriesAPISync:
        return _AssetCategoriesAPISync(self._client)


class _AssetsAPIAsync(
    AssetCreateAPIAsyncMixin,
    AssetDeleteAPIAsyncMixin,
    AssetGetAPIAsyncMixin,
    AssetUpdateAPIAsyncMixin,
    AssetReplaceAPIAsyncMixin,
    AssetsSearchAPIAsyncMixin,
):
    @property
    def categories(self) -> _AssetCategoriesAPIAsync:
        return _AssetCategoriesAPIAsync(self._client)


# Filters API
class _FiltersAPISync(
    FiltersGetAPISyncMixin,
): ...  # noqa: E701


class _FiltersAPIAsync(
    FiltersGetAPIAsyncMixin,
): ...  # noqa: E701


# Products API
class _ProductAssetsAPISync(
    ProductAssetsGetAPISyncMixin,
    ProductAssetLinkAPISyncMixin,
    ProductAssetUnlinkAPISyncMixin,
): ...  # noqa: E701


class _ProductAssetsAPIAsync(
    ProductAssetsGetAPIAsyncMixin,
    ProductAssetLinkAPIAsyncMixin,
    ProductAssetUnlinkAPIAsyncMixin,
): ...  # noqa: E701


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


class _ProductCategoriesAPISync(
    ProductCategoryCreateAPISyncMixin,
    ProductCategoryDeleteAPISyncMixin,
    ProductCategoryUpdateAPISyncMixin,
    ProductCategoriesSearchAPISyncMixin,
    ProductCategoryLinkAPISyncMixin,
    ProductCategoryUnlinkAPISyncMixin,
    ProductCategoriesGetAPISyncMixin,
): ...  # noqa: E701


class _ProductCategoriesAPIAsync(
    ProductCategoryCreateAPIAsyncMixin,
    ProductCategoryDeleteAPIAsyncMixin,
    ProductCategoryUpdateAPIAsyncMixin,
    ProductCategoriesSearchAPIAsyncMixin,
    ProductCategoryLinkAPIAsyncMixin,
    ProductCategoryUnlinkAPIAsyncMixin,
    ProductCategoriesGetAPIAsyncMixin,
): ...  # noqa: E701


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


class _ProductFamiliesAPIAsync(
    ProductFamilyCreateAPIAsyncMixin,
    ProductFamiliesSearchAPIAsyncMixin,
    ProductFamilyGetAPIAsyncMixin,
    ProductFamilyUpdateAPIAsyncMixin,
    ProductFamilyDeleteAPIAsyncMixin,
):
    @property
    def attributes(self) -> _ProductFamiliesAttributesAPIAsync:
        return _ProductFamiliesAttributesAPIAsync(self._client)


class _ProductVariantsAPISync(
    ProductVariantLinkAPISyncMixin,
    ProductVariantsGetAPISyncMixin,
): ...  # noqa: E701


class _ProductVariantsAPIAsync(
    ProductVariantLinkAPIAsyncMixin,
    ProductVariantsGetAPIAsyncMixin,
): ...  # noqa: E701


class _ProductsAPISync(
    ProductCreateAPISyncMixin,
    ProductsSearchAPISyncMixin,
    ProductGetAPISyncMixin,
    ProductUpdateAPISyncMixin,
    ProductDeleteAPISyncMixin,
    ProductFamilyAssignAPISyncMixin,
):
    @property
    def assets(self) -> _ProductAssetsAPISync:
        return _ProductAssetsAPISync(self._client)

    @property
    def attributes(self) -> _ProductAttributesAPISync:
        return _ProductAttributesAPISync(self._client)

    @property
    def categories(self) -> _ProductCategoriesAPISync:
        return _ProductCategoriesAPISync(self._client)

    @property
    def families(self) -> _ProductFamiliesAPISync:
        return _ProductFamiliesAPISync(self._client)

    @property
    def variants(self) -> _ProductVariantsAPISync:
        return _ProductVariantsAPISync(self._client)


class _ProductsAPIAsync(
    ProductCreateAPIAsyncMixin,
    ProductsSearchAPIAsyncMixin,
    ProductGetAPIAsyncMixin,
    ProductUpdateAPIAsyncMixin,
    ProductDeleteAPIAsyncMixin,
    ProductFamilyAssignAPIAsyncMixin,
):
    @property
    def assets(self) -> _ProductAssetsAPIAsync:
        return _ProductAssetsAPIAsync(self._client)

    @property
    def attributes(self) -> _ProductAttributesAPIAsync:
        return _ProductAttributesAPIAsync(self._client)

    @property
    def categories(self) -> _ProductCategoriesAPIAsync:
        return _ProductCategoriesAPIAsync(self._client)

    @property
    def families(self) -> _ProductFamiliesAPIAsync:
        return _ProductFamiliesAPIAsync(self._client)

    @property
    def variants(self) -> _ProductVariantsAPIAsync:
        return _ProductVariantsAPIAsync(self._client)
