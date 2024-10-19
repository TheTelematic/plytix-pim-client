import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus, HTTPMethod
from typing import List, TypedDict

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.products.relationship import ProductRelationship
from plytix_pim_client.dtos.request import PlytixRequest


class ProductRelationshipsUpdateQuantityDict(TypedDict):
    product_id: str
    product_relationship_id: str
    related_product_id: str
    quantity: int


class ProductRelationshipsUpdateQuantityAPI:
    @classmethod
    def get_request(
        cls,
        product_id: str,
        product_relationship_id: str,
        related_product_id: str,
        quantity: int,
    ) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.PATCH,
            endpoint=(
                f"/api/v1/products/{product_id}/relationships/{product_relationship_id}/product/{related_product_id}"
            ),
            kwargs={"json": {"quantity": quantity}},
        )

    @classmethod
    def process_response(cls, response) -> ProductRelationship | None:
        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        return ProductRelationship.from_dict(response.json()["data"][0])


class ProductRelationshipsUpdateQuantityAPISyncMixin(BaseAPISyncMixin):
    def update_quantity_product_relationship(
        self,
        product_id: str,
        product_relationship_id: str,
        related_product_id: str,
        quantity: int,
    ) -> ProductRelationship | None:
        """
        Update the quantity of a product relationship.

        :return: The product relationship.
        """
        request = ProductRelationshipsUpdateQuantityAPI.get_request(
            product_id=product_id,
            product_relationship_id=product_relationship_id,
            related_product_id=related_product_id,
            quantity=quantity,
        )
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductRelationshipsUpdateQuantityAPI.process_response(response)

    def update_quantity_multiple_product_relationships(
        self, updates: list[ProductRelationshipsUpdateQuantityDict]
    ) -> List[ProductRelationship | None]:
        """
        Update the quantity of multiple product relationships. This uses threading to make the requests concurrently.

        :return: The product relationships.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.update_quantity_product_relationship, **update) for update in updates]
            return [future.result() for future in futures]


class ProductRelationshipsUpdateQuantityAPIAsyncMixin(BaseAPIAsyncMixin):
    async def update_quantity_product_relationship(
        self,
        product_id: str,
        product_relationship_id: str,
        related_product_id: str,
        quantity: int,
    ) -> ProductRelationship | None:
        """
        Update the quantity of a product relationship.

        :return: The product relationship.
        """
        request = ProductRelationshipsUpdateQuantityAPI.get_request(
            product_id=product_id,
            product_relationship_id=product_relationship_id,
            related_product_id=related_product_id,
            quantity=quantity,
        )
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductRelationshipsUpdateQuantityAPI.process_response(response)

    async def update_quantity_multiple_product_relationships(
        self, updates: list[ProductRelationshipsUpdateQuantityDict]
    ) -> List[ProductRelationship | None]:
        """
        Update the quantity of multiple product relationships. This uses threading to make the requests concurrently.

        :return: The product relationships.
        """
        return list(await asyncio.gather(*[self.update_quantity_product_relationship(**update) for update in updates]))
