import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus, HTTPMethod
from typing import List

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.products.variant import ProductVariant
from plytix_pim_client.dtos.request import PlytixRequest


class ProductVariantsGetAPI:
    @classmethod
    def get_request(cls, **data) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.GET,
            endpoint=f"/api/v1/products/{data['product_id']}/variants",
        )

    @classmethod
    def process_response(cls, response) -> List[ProductVariant] | None:
        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        if data := response.json().get("data", []):
            return [ProductVariant.from_dict(item) for item in data]

        return []


class ProductVariantsGetAPISyncMixin(BaseAPISyncMixin):
    def get_product_variants(self, product_id: str) -> List[ProductVariant] | None:
        """
        Get the product variants.

        :return: The product variants.
        """
        request = ProductVariantsGetAPI.get_request(product_id=product_id)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductVariantsGetAPI.process_response(response)

    def get_multiple_product_variants(self, product_ids: list[str]) -> List[List[ProductVariant] | None]:
        """
        Get the variants for multiple products. This uses threading to make the requests concurrently.

        :return: The product variants.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.get_product_variants, product_id) for product_id in product_ids]
            return [future.result() for future in futures]


class ProductVariantsGetAPIAsyncMixin(BaseAPIAsyncMixin):
    async def get_product_variants(self, product_id: str) -> List[ProductVariant] | None:
        """
        Get the product variants.

        :return: The product variants.
        """
        request = ProductVariantsGetAPI.get_request(product_id=product_id)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductVariantsGetAPI.process_response(response)

    async def get_multiple_product_variants(self, product_ids: list[str]) -> List[List[ProductVariant] | None]:
        """
        Get the variants for multiple products. This uses threading to make the requests concurrently.

        :return: The product variants.
        """
        return list(await asyncio.gather(*[self.get_product_variants(product_id) for product_id in product_ids]))
