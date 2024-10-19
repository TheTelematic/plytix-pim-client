import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPMethod, HTTPStatus
from typing import TypedDict

import httpx

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.request import PlytixRequest


class ProductRelationshipsUnlinkDict(TypedDict):
    product_id: str
    product_relationship_id: str
    product_ids_to_unlink: list[str]


class ProductRelationshipsUnlinkAPI:
    @staticmethod
    def get_request(
        product_id: str,
        product_relationship_id: str,
        product_ids_to_unlink: list[str],
    ) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.POST,
            endpoint=f"api/v1/products/{product_id}/relationships/{product_relationship_id}/unlink",
            kwargs={
                "json": {"product_relationships": product_ids_to_unlink},
            },
        )

    @staticmethod
    def process_response(response: httpx.Response) -> bool:
        if response.status_code in [
            HTTPStatus.NOT_FOUND,
        ]:
            return False

        return True


class ProductRelationshipsUnlinkAPISyncMixin(BaseAPISyncMixin):
    def unlink_product_from_relationship(
        self,
        product_id: str,
        product_relationship_id: str,
        product_ids_to_unlink: list[str],
    ) -> bool:
        """
        Unlink product from a relationship.

        :return: If unlinked successfully.
        """
        request = ProductRelationshipsUnlinkAPI.get_request(product_id, product_relationship_id, product_ids_to_unlink)
        response = self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductRelationshipsUnlinkAPI.process_response(response)

    def unlink_product_from_relationships(self, unlinks: list[ProductRelationshipsUnlinkDict]) -> list[bool]:
        """
        Unlink multiple products from relationships. This uses threading to make the requests concurrently.

        :return: If unlinked successfully each.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.unlink_product_from_relationship, **unlink) for unlink in unlinks]
            return [future.result() for future in futures]


class ProductRelationshipsUnlinkAPIAsyncMixin(BaseAPIAsyncMixin):
    async def unlink_product_from_relationship(
        self,
        product_id: str,
        product_relationship_id: str,
        product_ids_to_unlink: list[str],
    ) -> bool:
        """
        Unlink product from a relationship.

        :return: If unlinked successfully.
        """
        request = ProductRelationshipsUnlinkAPI.get_request(product_id, product_relationship_id, product_ids_to_unlink)
        response = await self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductRelationshipsUnlinkAPI.process_response(response)

    async def unlink_product_from_relationships(self, unlinks: list[ProductRelationshipsUnlinkDict]) -> list[bool]:
        """
        Unlink multiple products from relationships. This uses asyncio to make the requests concurrently.

        :return: If unlinked successfully each.
        """
        return list(await asyncio.gather(*[self.unlink_product_from_relationship(**unlink) for unlink in unlinks]))
