import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.delete import DeleteResourceAPI


class ProductRelationshipsDeleteAPI(DeleteResourceAPI):
    endpoint_prefix = "/api/v1/relationships"


class ProductRelationshipsDeleteAPISyncMixin(BaseAPISyncMixin):
    def delete_product_relationship(self, relationship_id: str) -> bool:
        """
        Delete a product relationship.

        :return: True if deleted, False if it didn't exist.
        """
        request = ProductRelationshipsDeleteAPI.get_request(relationship_id)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductRelationshipsDeleteAPI.process_response(response)

    def delete_product_relationships(self, relationship_ids: list[str]) -> list[bool]:
        """
        Delete multiple product relationships. This uses threading to make the requests concurrently.

        :return: List of boolean. True if deleted, False if it didn't exist.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.delete_product_relationship, relationship_id)
                for relationship_id in relationship_ids
            ]
            return [future.result() for future in futures]


class ProductRelationshipsDeleteAPIAsyncMixin(BaseAPIAsyncMixin):
    async def delete_product_relationship(self, relationship_id: str) -> bool:
        """
        Delete a product relationship.

        :return: True if deleted, False if it didn't exist.
        """
        request = ProductRelationshipsDeleteAPI.get_request(relationship_id)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductRelationshipsDeleteAPI.process_response(response)

    async def delete_product_relationships(self, relationship_ids: list[str]) -> list[bool]:
        """
        Delete multiple product relationships. This uses asyncio to make the requests concurrently.

        :return: List of boolean. True if deleted, False if it didn't exist.
        """
        return list(
            await asyncio.gather(
                *[self.delete_product_relationship(relationship_id) for relationship_id in relationship_ids]
            )
        )
