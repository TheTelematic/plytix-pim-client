import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus
from typing import Tuple

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.update import UpdateResourceAPI
from plytix_pim_client.dtos.products.attribute import ProductAttribute


class ProductAttributeUpdateAPI(UpdateResourceAPI):
    endpoint_prefix = "/api/v1/attributes/product"
    resource_dto_class = ProductAttribute


class ProductAttributeUpdateAPISyncMixin(BaseAPISyncMixin):
    def update_attribute(self, attribute_id: str, new_name: str) -> ProductAttribute | None:
        """
        Update a product attribute.

        :return: The product attribute if exists, None otherwise.
        """
        data = {"name": new_name}
        request = ProductAttributeUpdateAPI.get_request(attribute_id, data)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductAttributeUpdateAPI.process_response(response)

    def update_attributes(self, attribute_ids_with_new_name: list[Tuple[str, str]]) -> list[ProductAttribute | None]:
        """
        Update multiple products attributes. This uses threading to make the requests concurrently.

        :return: List of product attributes and/or None if any doesn't exist.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.update_attribute, attribute_id, new_name)
                for attribute_id, new_name in attribute_ids_with_new_name
            ]
            return [future.result() for future in futures]


class ProductAttributeUpdateAPIAsyncMixin(BaseAPIAsyncMixin):
    async def update_attribute(self, attribute_id: str, new_name: str) -> ProductAttribute | None:
        """
        Update a product attribute.

        :return: The product attribute if exists, None otherwise.
        """
        data = {"name": new_name}
        request = ProductAttributeUpdateAPI.get_request(attribute_id, data)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductAttributeUpdateAPI.process_response(response)

    async def update_attributes(
        self, attribute_ids_with_new_name: list[Tuple[str, str]]
    ) -> list[ProductAttribute | None]:
        """
        Update multiple products attributes. This uses asyncio to make the requests concurrently.

        :return: List of product attributes and/or None if any doesn't exist.
        """
        return list(
            await asyncio.gather(
                *[
                    self.update_attribute(attribute_id, new_name)
                    for attribute_id, new_name in attribute_ids_with_new_name
                ]
            )
        )
