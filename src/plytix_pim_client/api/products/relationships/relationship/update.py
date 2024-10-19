import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus
from typing import Tuple

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.update import UpdateResourceAPI
from plytix_pim_client.dtos.products.relationship import ProductRelationship


class ProductRelationshipUpdateAPI(UpdateResourceAPI):
    endpoint_prefix = "/api/v1/relationships"
    resource_dto_class = ProductRelationship


class ProductRelationshipUpdateAPISyncMixin(BaseAPISyncMixin):
    def update_relationship(self, relationship_id: str, new_name: str) -> ProductRelationship | None:
        """
        Update a product relationship.

        :return: The product relationship if exists, None otherwise.
        """
        data = {"name": new_name}
        request = ProductRelationshipUpdateAPI.get_request(relationship_id, data)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductRelationshipUpdateAPI.process_response(response)

    def update_relationships(
        self, relationship_ids_with_new_name: list[Tuple[str, str]]
    ) -> list[ProductRelationship | None]:
        """
        Update multiple products relationships. This uses threading to make the requests concurrently.

        :return: List of product relationships and/or None if any doesn't exist.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.update_relationship, relationship_id, new_name)
                for relationship_id, new_name in relationship_ids_with_new_name
            ]
            return [future.result() for future in futures]


class ProductRelationshipUpdateAPIAsyncMixin(BaseAPIAsyncMixin):
    async def update_relationship(self, relationship_id: str, new_name: str) -> ProductRelationship | None:
        """
        Update a product relationship.

        :return: The product relationship if exists, None otherwise.
        """
        data = {"name": new_name}
        request = ProductRelationshipUpdateAPI.get_request(relationship_id, data)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductRelationshipUpdateAPI.process_response(response)

    async def update_relationships(
        self, relationship_ids_with_new_name: list[Tuple[str, str]]
    ) -> list[ProductRelationship | None]:
        """
        Update multiple products relationships. This uses asyncio to make the requests concurrently.

        :return: List of product relationships and/or None if any doesn't exist.
        """
        return list(
            await asyncio.gather(
                *[
                    self.update_relationship(relationship_id, new_name)
                    for relationship_id, new_name in relationship_ids_with_new_name
                ]
            )
        )
