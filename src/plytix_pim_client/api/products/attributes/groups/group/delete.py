import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.delete import DeleteResourceAPI


class ProductAttributesGroupDeleteAPI(DeleteResourceAPI):
    endpoint_prefix = "/api/v1/attribute-groups/product"


class ProductAttributesGroupDeleteAPISyncMixin(BaseAPISyncMixin):
    def delete_attributes_group(self, attributes_group_id: str) -> bool:
        """
        Delete a product attributes_group.

        :return: True if deleted, False if it didn't exist.
        """
        request = ProductAttributesGroupDeleteAPI.get_request(attributes_group_id)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductAttributesGroupDeleteAPI.process_response(response)

    def delete_attributes_groups(self, attributes_group_ids: list[str]) -> list[bool]:
        """
        Delete multiple products attributes_groups. This uses threading to make the requests concurrently.

        :return: List of boolean. True if deleted, False if it didn't exist.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.delete_attributes_group, attributes_group_id)
                for attributes_group_id in attributes_group_ids
            ]
            return [future.result() for future in futures]


class ProductAttributesGroupDeleteAPIAsyncMixin(BaseAPIAsyncMixin):
    async def delete_attributes_group(self, attributes_group_id: str) -> bool:
        """
        Delete a product attributes_group.

        :return: True if deleted, False if it didn't exist.
        """
        request = ProductAttributesGroupDeleteAPI.get_request(attributes_group_id)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductAttributesGroupDeleteAPI.process_response(response)

    async def delete_attributes_groups(self, attributes_group_ids: list[str]) -> list[bool]:
        """
        Delete multiple products attributes_groups. This uses asyncio to make the requests concurrently.

        :return: List of boolean. True if deleted, False if it didn't exist.
        """
        return list(
            await asyncio.gather(
                *[self.delete_attributes_group(attributes_group_id) for attributes_group_id in attributes_group_ids]
            )
        )
