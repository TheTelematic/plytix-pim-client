from http import HTTPMethod, HTTPStatus
from typing import TypedDict

import httpx

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.products.relationship import ProductRelationship, ProductRelationshipRelatedProduct
from plytix_pim_client.dtos.request import PlytixRequest


class ProductRelationshipDict(TypedDict):
    product_id: str
    quantity: int


class ProductRelationshipsDict(TypedDict):
    product_id: str
    product_relationship_id: str
    product_relationships: list[ProductRelationshipDict]


class ProductRelationshipLinkAPI:
    @staticmethod
    def get_request(
        product_id: str,
        product_relationship_id: str,
        product_relationships: list[ProductRelationshipDict],
    ) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.POST,
            endpoint=f"api/v1/products/{product_id}/relationships/{product_relationship_id}",
            kwargs={"json": {"product_relationships": [pr for pr in product_relationships]}},
        )

    @staticmethod
    def process_response(response: httpx.Response) -> ProductRelationship | None:
        if response.status_code in [
            HTTPStatus.NOT_FOUND,
        ]:
            return None

        data = response.json()["data"][0]
        return ProductRelationship(
            id=data["relationship_id"],
            label=data["relationship_label"],
            related_products=[ProductRelationshipRelatedProduct.from_dict(rp) for rp in data["related_products"]],
        )


class ProductRelationshipLinkAPISyncMixin(BaseAPISyncMixin):
    def link_product_to_relationship(
        self,
        product_id: str,
        product_relationship_id: str,
        product_relationships: list[ProductRelationshipDict],
    ) -> ProductRelationship | None:
        """
        Link product to a relationship.

        :return: If linked successfully.
        """
        request = ProductRelationshipLinkAPI.get_request(product_id, product_relationship_id, product_relationships)
        response = self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductRelationshipLinkAPI.process_response(response)

    def link_product_to_relationships(
        self, relationships: list[ProductRelationshipsDict]
    ) -> list[ProductRelationship | None]:
        """
        Link products to relationships.
        This NOT uses threading to make the requests concurrently, due to race condition on server side.

        :return: If linked successfully each.
        """
        return [self.link_product_to_relationship(**relationship) for relationship in relationships]


class ProductRelationshipLinkAPIAsyncMixin(BaseAPIAsyncMixin):
    async def link_product_to_relationship(
        self,
        product_id: str,
        product_relationship_id: str,
        product_relationships: list[ProductRelationshipDict],
    ) -> ProductRelationship | None:
        """
        Link product to a relationship.

        :return: If linked successfully.
        """
        request = ProductRelationshipLinkAPI.get_request(product_id, product_relationship_id, product_relationships)
        response = await self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductRelationshipLinkAPI.process_response(response)

    async def link_product_to_relationships(
        self, relationships: list[ProductRelationshipsDict]
    ) -> list[ProductRelationship | None]:
        """
        Link products to relationships.
        This NOT uses asyncio to make the requests concurrently, due to race condition on server side.

        :return: If linked successfully each.
        """
        return [await self.link_product_to_relationship(**relationship) for relationship in relationships]
