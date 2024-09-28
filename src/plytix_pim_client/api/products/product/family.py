import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPMethod, HTTPStatus
from typing import Tuple

import httpx

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.request import PlytixRequest


class ProductFamilyAssignAPI:
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


class ProductFamilyAssignAPISyncMixin(BaseAPISyncMixin):
    def assign_family(self, product_id: str, product_family_id: str) -> bool | None:
        """
        Assign a family to product.

        :return: The product.
        """
        request = ProductFamilyAssignAPI.get_request(product_id, product_family_id)
        response = self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[HTTPStatus.NOT_FOUND, HTTPStatus.INTERNAL_SERVER_ERROR],
            **request.kwargs,
        )
        return ProductFamilyAssignAPI.process_response(response)

    def assign_families(self, product_ids_and_family_ids: list[Tuple[str, str]]) -> list[bool | None]:
        """
        Assign a family to multiple products. This uses threading to make the requests concurrently.

        :return: The products.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.assign_family, product_id, product_family_id)
                for product_id, product_family_id in product_ids_and_family_ids
            ]
            return [future.result() for future in futures]


class ProductFamilyAssignAPIAsyncMixin(BaseAPIAsyncMixin):
    async def assign_family(self, product_id: str, product_family_id: str) -> bool | None:
        """
        Assign a family to a product.

        :return: The product.
        """
        request = ProductFamilyAssignAPI.get_request(product_id, product_family_id)
        response = await self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[HTTPStatus.NOT_FOUND, HTTPStatus.INTERNAL_SERVER_ERROR],
            **request.kwargs,
        )
        return ProductFamilyAssignAPI.process_response(response)

    async def assign_families(self, product_ids_and_family_ids: list[Tuple[str, str]]) -> list[bool | None]:
        """
        Assign a family to multiple products. This uses asyncio to make the requests concurrently.

        :return: The products.
        """
        return list(
            await asyncio.gather(
                *[
                    self.assign_family(product_id, product_family_id)
                    for product_id, product_family_id in product_ids_and_family_ids
                ]
            )
        )
