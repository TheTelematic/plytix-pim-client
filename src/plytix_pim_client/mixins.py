from plytix_pim_client.api.products.attributes.attribute.create import (
    ProductAttributeCreateAPISyncMixin,
    ProductAttributeCreateAPIAsyncMixin,
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
    ProductAttributeUpdateAPISyncMixin,
    ProductAttributeUpdateAPIAsyncMixin,
)
from plytix_pim_client.api.products.attributes.search import (
    ProductAttributesSearchAPISyncMixin,
    ProductAttributesSearchAPIAsyncMixin,
)
from plytix_pim_client.api.products.families.family.attributes.get import (
    ProductFamilyGetAttributesAPISyncMixin,
    ProductFamilyGetAttributesAPIAsyncMixin,
)
from plytix_pim_client.api.products.families.family.attributes.inheritance import (
    ProductFamilyEditAttributeInheritanceAPISyncMixin,
    ProductFamilyEditAttributeInheritanceAPIAsyncMixin,
)
from plytix_pim_client.api.products.families.family.attributes.link import (
    ProductFamilyLinkAttributeAPISyncMixin,
    ProductFamilyLinkAttributeAPIAsyncMixin,
)
from plytix_pim_client.api.products.families.family.create import (
    ProductFamilyCreateAPISyncMixin,
    ProductFamilyCreateAPIAsyncMixin,
)
from plytix_pim_client.api.products.families.family.delete import (
    ProductFamilyDeleteAPISyncMixin,
    ProductFamilyDeleteAPIAsyncMixin,
)
from plytix_pim_client.api.products.families.family.get import (
    ProductFamilyGetAPISyncMixin,
    ProductFamilyGetAPIAsyncMixin,
)
from plytix_pim_client.api.products.families.family.update import (
    ProductFamilyUpdateAPISyncMixin,
    ProductFamilyUpdateAPIAsyncMixin,
)
from plytix_pim_client.api.products.families.search import (
    ProductFamiliesSearchAPISyncMixin,
    ProductFamiliesSearchAPIAsyncMixin,
)
from plytix_pim_client.api.products.product.create import ProductCreateAPISyncMixin, ProductCreateAPIAsyncMixin
from plytix_pim_client.api.products.product.delete import ProductDeleteAPISyncMixin, ProductDeleteAPIAsyncMixin
from plytix_pim_client.api.products.product.family import (
    ProductFamilyAssignAPISyncMixin,
    ProductFamilyAssignAPIAsyncMixin,
)
from plytix_pim_client.api.products.product.get import ProductGetAPISyncMixin, ProductGetAPIAsyncMixin
from plytix_pim_client.api.products.product.update import ProductUpdateAPISyncMixin, ProductUpdateAPIAsyncMixin
from plytix_pim_client.api.products.search import ProductsSearchAPISyncMixin, ProductsSearchAPIAsyncMixin


# Product Families Attributes API
class _ProductFamiliesAttributesAPISync(
    ProductFamilyGetAttributesAPISyncMixin,
    ProductFamilyLinkAttributeAPISyncMixin,
    ProductFamilyEditAttributeInheritanceAPISyncMixin,
): ...  # noqa: E701


class _ProductFamiliesAttributesAPIAsync(
    ProductFamilyGetAttributesAPIAsyncMixin,
    ProductFamilyLinkAttributeAPIAsyncMixin,
    ProductFamilyEditAttributeInheritanceAPIAsyncMixin,
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
