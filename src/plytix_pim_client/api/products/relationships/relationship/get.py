import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.get import GetResourceAPI
from plytix_pim_client.dtos.products.relationship import ProductRelationship


class ProductRelationshipGetAPI(GetResourceAPI):
    endpoint_prefix = "/api/v1/relationships"
    resource_dto_class = ProductRelationship


class ProductRelationshipGetAPISyncMixin(BaseAPISyncMixin):
    def get_relationship(self, relationship_id: str) -> ProductRelationship | None:
        """
        Get a product relationship.

        :return: The product relationship if exists, None otherwise.
        """
        request = ProductRelationshipGetAPI.get_request(relationship_id)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductRelationshipGetAPI.process_response(response)

    def get_relationships(self, relationship_ids: list[str]) -> list[ProductRelationship | None]:
        """
        Get multiple products relationships. This uses threading to make the requests concurrently.

        :return: List of product relationships and/or None if any doesn't exist.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.get_relationship, relationship_id) for relationship_id in relationship_ids]
            return [future.result() for future in futures]


class ProductRelationshipGetAPIAsyncMixin(BaseAPIAsyncMixin):
    async def get_relationship(self, relationship_id: str) -> ProductRelationship | None:
        """
        Get a product relationship.

        :return: The product relationship if exists, None otherwise.
        """
        request = ProductRelationshipGetAPI.get_request(relationship_id)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductRelationshipGetAPI.process_response(response)

    async def get_relationships(self, relationship_ids: list[str]) -> list[ProductRelationship | None]:
        """
        Get multiple products relationships. This uses asyncio to make the requests concurrently.

        :return: List of product relationships and/or None if any doesn't exist.
        """
        return list(
            await asyncio.gather(*[self.get_relationship(relationship_id) for relationship_id in relationship_ids])
        )
