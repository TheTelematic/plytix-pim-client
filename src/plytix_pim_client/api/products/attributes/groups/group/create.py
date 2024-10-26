from typing import Dict, List, TypedDict, NotRequired

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.create import CreateResourceAPI
from plytix_pim_client.dtos.products.attribute import ProductAttributesGroup


class ProductAttributesGroupCreateDict(TypedDict):
    name: str
    attribute_labels: NotRequired[List[str]]
    order: NotRequired[int]


class ProductAttributesGroupCreateAPI(CreateResourceAPI):
    endpoint = "/api/v1/attribute-groups/product"
    resource_dto_class = ProductAttributesGroup


class ProductAttributesGroupCreateAPISyncMixin(BaseAPISyncMixin):
    def create_attributes_group(
        self,
        name: str,
        attribute_labels: List[str] | None = None,
        order: int | None = None,
    ) -> ProductAttributesGroup:
        """
        Create a product attributes group.

        :return: The product attributes group created.
        """
        data: Dict[str, str | List[str] | int] = {
            "name": name,
        }
        if attribute_labels:
            data["attribute_labels"] = attribute_labels
        if order:
            data["order"] = order

        request = ProductAttributesGroupCreateAPI.get_request(**data)
        response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductAttributesGroupCreateAPI.process_response(response)

    def create_attributes_groups(self, groups: list[ProductAttributesGroupCreateDict]) -> list[ProductAttributesGroup]:
        """
        Create multiple product attributes groups.
        This NOT uses threading to make the requests concurrently, due to race condition on server side.

        :return: The product attributes groups created.
        """
        return [self.create_attributes_group(**group) for group in groups]


class ProductAttributesGroupCreateAPIAsyncMixin(BaseAPIAsyncMixin):
    async def create_attributes_group(
        self,
        name: str,
        attribute_labels: List[str] | None = None,
        order: int | None = None,
    ) -> ProductAttributesGroup:
        """
        Create a product attributes group.

        :return: The product attributes group created.
        """
        data: Dict[str, str | List[str] | int] = {
            "name": name,
        }
        if attribute_labels:
            data["attribute_labels"] = attribute_labels
        if order:
            data["order"] = order

        request = ProductAttributesGroupCreateAPI.get_request(**data)
        response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductAttributesGroupCreateAPI.process_response(response)

    async def create_attributes_groups(
        self, groups: list[ProductAttributesGroupCreateDict]
    ) -> list[ProductAttributesGroup]:
        """
        Create multiple product attributes groups.
        This NOT uses asyncio to make the requests concurrently, due to race condition on server side.

        :return: If linked successfully each.
        """
        return [await self.create_attributes_group(**group) for group in groups]
