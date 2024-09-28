import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPMethod, HTTPStatus
from typing import List

import httpx

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.products.family import ProductFamilyAttribute
from plytix_pim_client.dtos.request import PlytixRequest


class ProductFamilyGetAttributesAPI:
    @staticmethod
    def get_request(product_family_id: str) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.GET,
            endpoint=f"api/v1/product_families/{product_family_id}/attributes",
        )

    @staticmethod
    def process_response(response: httpx.Response) -> List[ProductFamilyAttribute] | None:
        if response.status_code in [
            HTTPStatus.NOT_FOUND,
        ]:
            return None

        return [ProductFamilyAttribute.from_dict(data) for data in response.json()["data"]]


class ProductFamilyGetAttributesAPISyncMixin(BaseAPISyncMixin):
    def get_family_attributes(self, product_family_id: str) -> List[ProductFamilyAttribute] | None:
        """
        Assign a family to product.

        :return: The product.
        """
        request = ProductFamilyGetAttributesAPI.get_request(product_family_id)
        response = self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductFamilyGetAttributesAPI.process_response(response)

    def get_families_attributes(self, product_family_ids: List[str]) -> List[List[ProductFamilyAttribute] | None]:
        """
        Assign a family to multiple products. This uses threading to make the requests concurrently.

        :return: The products.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.get_family_attributes, product_family_id)
                for product_family_id in product_family_ids
            ]
            return [future.result() for future in futures]


class ProductFamilyGetAttributesAPIAsyncMixin(BaseAPIAsyncMixin):
    async def get_family_attributes(self, product_family_id: str) -> List[ProductFamilyAttribute] | None:
        """
        Assign a family to a product.

        :return: The product.
        """
        request = ProductFamilyGetAttributesAPI.get_request(product_family_id)
        response = await self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductFamilyGetAttributesAPI.process_response(response)

    async def get_families_attributes(self, product_family_ids: List[str]) -> List[List[ProductFamilyAttribute] | None]:
        """
        Assign a family to multiple products. This uses asyncio to make the requests concurrently.

        :return: The products.
        """
        return list(
            await asyncio.gather(
                *[self.get_family_attributes(product_family_id) for product_family_id in product_family_ids]
            )
        )
