import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus
from typing import TypedDict, List, NotRequired, Dict

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.update import UpdateResourceAPI
from plytix_pim_client.dtos.products.attribute import ProductAttributesGroup


class ProductAttributesGroupUpdateDict(TypedDict):
    attributes_group_id: str
    name: NotRequired[str]
    attribute_labels: NotRequired[List[str]]
    order: NotRequired[int]


class ProductAttributesGroupUpdateAPI(UpdateResourceAPI):
    endpoint_prefix = "/api/v1/attribute-groups/product"
    resource_dto_class = ProductAttributesGroup


class ProductAttributesGroupUpdateAPISyncMixin(BaseAPISyncMixin):
    def update_attributes_group(
        self,
        attributes_group_id: str,
        name: str | None = None,
        attribute_labels: List[str] | None = None,
        order: int | None = None,
    ) -> ProductAttributesGroup | None:
        """
        Update a product attributes group.

        :return: The product attributes group if exists, None otherwise.
        """
        data: Dict[str, str | List[str] | int] = {}
        if name:
            data["name"] = name
        if attribute_labels:
            data["attribute_labels"] = attribute_labels
        if order:
            data["order"] = order

        request = ProductAttributesGroupUpdateAPI.get_request(attributes_group_id, data)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductAttributesGroupUpdateAPI.process_response(response)

    def update_attributes_groups(
        self, groups: list[ProductAttributesGroupUpdateDict]
    ) -> list[ProductAttributesGroup | None]:
        """
        Update multiple products attributes. This uses threading to make the requests concurrently.

        :return: List of product attributes groups and/or None if any doesn't exist.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.update_attributes_group, **group) for group in groups]
            return [future.result() for future in futures]


class ProductAttributesGroupUpdateAPIAsyncMixin(BaseAPIAsyncMixin):
    async def update_attributes_group(
        self,
        attributes_group_id: str,
        name: str | None = None,
        attribute_labels: List[str] | None = None,
        order: int | None = None,
    ) -> ProductAttributesGroup | None:
        """
        Update a product attributes group.

        :return: The product attributes group if exists, None otherwise.
        """
        data: Dict[str, str | List[str] | int] = {}
        if name:
            data["name"] = name
        if attribute_labels:
            data["attribute_labels"] = attribute_labels
        if order:
            data["order"] = order

        request = ProductAttributesGroupUpdateAPI.get_request(attributes_group_id, data)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductAttributesGroupUpdateAPI.process_response(response)

    async def update_attributes_groups(
        self, groups: list[ProductAttributesGroupUpdateDict]
    ) -> list[ProductAttributesGroup | None]:
        """
        Update multiple products attributes. This uses threading to make the requests concurrently.

        :return: List of product attributes groups and/or None if any doesn't exist.
        """
        return list(await asyncio.gather(*[self.update_attributes_group(**group) for group in groups]))
