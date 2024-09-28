import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.get import GetResourceAPI
from plytix_pim_client.dtos.products.attribute import ProductAttribute


class ProductAttributeGetAPI(GetResourceAPI):
    endpoint_prefix = "/api/v1/attributes/product"
    resource_dto_class = ProductAttribute


class ProductAttributeGetAPISyncMixin(BaseAPISyncMixin):
    def get_attribute(self, attribute_id: str) -> ProductAttribute | None:
        """
        Get a product attribute.

        :return: The product attribute if exists, None otherwise.
        """
        request = ProductAttributeGetAPI.get_request(attribute_id)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductAttributeGetAPI.process_response(response)

    def get_attributes(self, attribute_ids: list[str]) -> list[ProductAttribute | None]:
        """
        Get multiple products attributes. This uses threading to make the requests concurrently.

        :return: List of product attributes and/or None if any doesn't exist.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.get_attribute, attribute_id) for attribute_id in attribute_ids]
            return [future.result() for future in futures]


class ProductAttributeGetAPIAsyncMixin(BaseAPIAsyncMixin):
    async def get_attribute(self, attribute_id: str) -> ProductAttribute | None:
        """
        Get a product attribute.

        :return: The product attribute if exists, None otherwise.
        """
        request = ProductAttributeGetAPI.get_request(attribute_id)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductAttributeGetAPI.process_response(response)

    async def get_attributes(self, attribute_ids: list[str]) -> list[ProductAttribute | None]:
        """
        Get multiple products attributes. This uses asyncio to make the requests concurrently.

        :return: List of product attributes and/or None if any doesn't exist.
        """
        return list(await asyncio.gather(*[self.get_attribute(attribute_id) for attribute_id in attribute_ids]))
