import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.delete import DeleteResourceAPI


class ProductAttributeDeleteAPI(DeleteResourceAPI):
    endpoint_prefix = "/api/v1/attributes/product"


class ProductAttributeDeleteAPISyncMixin(BaseAPISyncMixin):
    def delete_attribute(self, attribute_id: str) -> bool:
        """
        Delete a product attribute.

        :return: True if deleted, False if it didn't exist.
        """
        request = ProductAttributeDeleteAPI.get_request(attribute_id)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductAttributeDeleteAPI.process_response(response)

    def delete_attributes(self, attribute_ids: list[str]) -> list[bool]:
        """
        Delete multiple products attributes. This uses threading to make the requests concurrently.

        :return: List of boolean. True if deleted, False if it didn't exist.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.delete_attribute, attribute_id) for attribute_id in attribute_ids]
            return [future.result() for future in futures]


class ProductAttributeDeleteAPIAsyncMixin(BaseAPIAsyncMixin):
    async def delete_attribute(self, attribute_id: str) -> bool:
        """
        Delete a product attribute.

        :return: True if deleted, False if it didn't exist.
        """
        request = ProductAttributeDeleteAPI.get_request(attribute_id)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductAttributeDeleteAPI.process_response(response)

    async def delete_attributes(self, attribute_ids: list[str]) -> list[bool]:
        """
        Delete multiple products attributes. This uses asyncio to make the requests concurrently.

        :return: List of boolean. True if deleted, False if it didn't exist.
        """
        return list(await asyncio.gather(*[self.delete_attribute(attribute_id) for attribute_id in attribute_ids]))
