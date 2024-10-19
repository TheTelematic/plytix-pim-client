import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from typing import TypedDict

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.create import CreateResourceAPI
from plytix_pim_client.dtos.products.relationship import ProductRelationship


class CreateProductRelationshipDict(TypedDict):
    name: str


class ProductRelationshipCreateAPI(CreateResourceAPI):
    endpoint = "/api/v1/relationships"
    resource_dto_class = ProductRelationship


class ProductRelationshipCreateAPISyncMixin(BaseAPISyncMixin):
    def create_product_relationship(self, name: str) -> ProductRelationship:
        """
        Create a product relationship.

        :return: The product relationship created.
        """
        request = ProductRelationshipCreateAPI.get_request(name=name)
        response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductRelationshipCreateAPI.process_response(response)

    def create_product_relationships(
        self, product_relationships: list[CreateProductRelationshipDict]
    ) -> list[ProductRelationship]:
        """
        Create multiple product relationships. This uses threading to make the requests concurrently.

        :return: The product relationships created.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.create_product_relationship, **relationship)
                for relationship in product_relationships
            ]
            return [future.result() for future in futures]


class ProductRelationshipCreateAPIAsyncMixin(BaseAPIAsyncMixin):
    async def create_product_relationship(
        self, name: str, parent_relationship_id: str | None = None
    ) -> ProductRelationship:
        """
        Create a product relationship.

        :return: The product relationship created.
        """
        request = ProductRelationshipCreateAPI.get_request(name=name, parent_relationship_id=parent_relationship_id)
        response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductRelationshipCreateAPI.process_response(response)

    async def create_product_relationships(
        self, product_relationships: list[CreateProductRelationshipDict]
    ) -> list[ProductRelationship]:
        """
        Create multiple product relationships. This uses asyncio to make the requests concurrently.

        :return: The product relationships created.
        """
        return list(
            await asyncio.gather(
                *[self.create_product_relationship(**relationship) for relationship in product_relationships]
            )
        )
