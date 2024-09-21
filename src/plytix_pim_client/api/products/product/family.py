import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPMethod, HTTPStatus
from typing import Tuple

import httpx

from plytix_pim_client.api.base import BaseAPISyncMixin, BaseAPIAsyncMixin
from plytix_pim_client.dtos.request import PlytixRequest


class ProductAssignFamilyAPI:
    @staticmethod
    def get_request(product_id: str, product_family_id: str) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.POST,
            endpoint=f"/api/v1/products/{product_id}/family",
            kwargs={"json": {"product_family_id": product_family_id}},
        )

    @staticmethod
    def process_response(response: httpx.Response) -> bool | None:
        if response.status_code in [HTTPStatus.NOT_FOUND, HTTPStatus.INTERNAL_SERVER_ERROR]:
            return None

        return True


class ProductAssignFamilyAPISyncMixin(BaseAPISyncMixin):
    def assign_family_to_product(self, product_id: str, product_family_id: str) -> bool | None:
        """
        Assign a family to product.

        :return: The product.
        """
        request = ProductAssignFamilyAPI.get_request(product_id, product_family_id)
        response = self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[HTTPStatus.NOT_FOUND, HTTPStatus.INTERNAL_SERVER_ERROR],
            **request.kwargs,
        )
        return ProductAssignFamilyAPI.process_response(response)

    def assign_family_to_products(self, product_ids_and_family_ids: list[Tuple[str, str]]) -> list[bool | None]:
        """
        Assign a family to multiple products. This uses threading to make the requests concurrently.

        :return: The products.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.assign_family_to_product, product_id, product_family_id)
                for product_id, product_family_id in product_ids_and_family_ids
            ]
            return [future.result() for future in futures]


class ProductAssignFamilyAPIAsyncMixin(BaseAPIAsyncMixin):
    async def assign_family_to_product(self, product_id: str, product_family_id: str) -> bool | None:
        """
        Assign a family to a product.

        :return: The product.
        """
        request = ProductAssignFamilyAPI.get_request(product_id, product_family_id)
        response = await self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[HTTPStatus.NOT_FOUND, HTTPStatus.INTERNAL_SERVER_ERROR],
            **request.kwargs,
        )
        return ProductAssignFamilyAPI.process_response(response)

    async def assign_family_to_products(self, product_ids_and_family_ids: list[Tuple[str, str]]) -> list[bool | None]:
        """
        Assign a family to multiple products. This uses asyncio to make the requests concurrently.

        :return: The products.
        """
        return list(
            await asyncio.gather(
                *[
                    self.assign_family_to_product(product_id, product_family_id)
                    for product_id, product_family_id in product_ids_and_family_ids
                ]
            )
        )
