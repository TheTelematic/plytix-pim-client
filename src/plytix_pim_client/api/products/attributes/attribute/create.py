import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from typing import TypedDict, List

from plytix_pim_client.api.base import BaseAPISyncMixin, BaseAPIAsyncMixin
from plytix_pim_client.api.common.create import CreateResourceAPI
from plytix_pim_client.dtos.family import AttributeLevel
from plytix_pim_client.dtos.products.attribute import ProductAttribute, ProductAttributeTypeClass


class CreateProductAttributeProductFamiliesDict(TypedDict):
    id: str
    attribute_level: AttributeLevel


class CreateProductAttributeRelatedAttributesDict(TypedDict):
    id: str
    label: str


class CreateProductAttributeDict(TypedDict):
    name: str
    type_class: ProductAttributeTypeClass
    description: str | None
    product_families: List[CreateProductAttributeProductFamiliesDict] | None
    options: List[str] | None
    manual_sorting: bool | None
    sort_ascending: bool | None
    attributes: List[CreateProductAttributeRelatedAttributesDict] | None


class CreateProductAttributeAPI(CreateResourceAPI):
    endpoint = "/api/v1/attributes/product"
    resource_dto_class = ProductAttribute


class ProductAttributeCreateAPISyncMixin(BaseAPISyncMixin):
    def create_product_attribute(
        self,
        name: str,
        type_class: ProductAttributeTypeClass,
        description: str | None = None,
        product_families: List[CreateProductAttributeProductFamiliesDict] | None = None,
        options: List[str] | None = None,
        manual_sorting: bool | None = None,
        sort_ascending: bool | None = None,
        attributes: List[CreateProductAttributeRelatedAttributesDict] | None = None,
    ) -> ProductAttribute:
        """
        Create a product attribute.

        :return: The product attribute created.
        """
        data = {
            "name": name,
            "type_class": type_class,
        }
        if description:
            data["description"] = description
        if product_families:
            data["product_families"] = product_families
        if options:
            data["options"] = options
        if manual_sorting:
            data["manual_sorting"] = manual_sorting
        if sort_ascending:
            data["sort_ascending"] = sort_ascending
        if attributes:
            data["attributes"] = attributes

        request = CreateProductAttributeAPI.get_request(**data)
        response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return CreateProductAttributeAPI.process_response(response)

    def create_product_attributes(self, product_attributes: list[CreateProductAttributeDict]) -> list[ProductAttribute]:
        """
        Create multiple product attributes. This uses threading to make the requests concurrently.

        :return: The product attributes created.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.create_product_attribute, **product_attribute)
                for product_attribute in product_attributes
            ]
            return [future.result() for future in futures]


class ProductAttributeCreateAPIAsyncMixin(BaseAPIAsyncMixin):
    async def create_product_attribute(
        self,
        name: str,
        type_class: ProductAttributeTypeClass,
        description: str | None = None,
        product_families: List[CreateProductAttributeProductFamiliesDict] | None = None,
        options: List[str] | None = None,
        manual_sorting: bool | None = None,
        sort_ascending: bool | None = None,
        attributes: List[CreateProductAttributeRelatedAttributesDict] | None = None,
    ) -> ProductAttribute:
        """
        Create a product attribute.

        :return: The product attribute created.
        """
        data = {
            "name": name,
            "type_class": type_class,
        }
        if description:
            data["description"] = description
        if product_families:
            data["product_families"] = product_families
        if options:
            data["options"] = options
        if manual_sorting:
            data["manual_sorting"] = manual_sorting
        if sort_ascending:
            data["sort_ascending"] = sort_ascending
        if attributes:
            data["attributes"] = attributes

        request = CreateProductAttributeAPI.get_request(**data)
        response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return CreateProductAttributeAPI.process_response(response)

    async def create_product_attributes(
        self, product_attributes: list[CreateProductAttributeDict]
    ) -> list[ProductAttribute]:
        """
        Create multiple product attributes. This uses asyncio to make the requests concurrently.

        :return: The product attributes created.
        """
        return list(
            await asyncio.gather(
                *[self.create_product_attribute(**product_attribute) for product_attribute in product_attributes]
            )
        )
