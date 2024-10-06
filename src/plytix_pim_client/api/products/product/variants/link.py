from http import HTTPMethod, HTTPStatus
from typing import Tuple

import httpx

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.request import PlytixRequest


class ProductVariantLinkAPI:
    @staticmethod
    def get_request(
        product_id: str,
        product_variant_id: str,
    ) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.POST,
            endpoint=f"api/v1/products/{product_id}/variant/{product_variant_id}",
        )

    @staticmethod
    def process_response(response: httpx.Response) -> bool:
        if response.status_code in [
            HTTPStatus.NOT_FOUND,
        ]:
            return False

        return True


class ProductVariantLinkAPISyncMixin(BaseAPISyncMixin):
    def link_variant_to_product(
        self,
        product_id: str,
        product_variant_id: str,
    ) -> bool:
        """
        Link variant to a product.

        :return: If linked successfully.
        """
        request = ProductVariantLinkAPI.get_request(product_id, product_variant_id)
        response = self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductVariantLinkAPI.process_response(response)

    def link_variant_to_products(self, product_ids_variant_ids: list[Tuple[str, str]]) -> list[bool]:
        """
        Link multiple variants to products.
        This NOT uses threading to make the requests concurrently, due to race condition on server side.

        :return: If linked successfully each.
        """
        return [
            self.link_variant_to_product(product_id, product_variant_id)
            for product_id, product_variant_id in product_ids_variant_ids
        ]


class ProductVariantLinkAPIAsyncMixin(BaseAPIAsyncMixin):
    async def link_variant_to_product(
        self,
        product_id: str,
        product_variant_id: str,
    ) -> bool:
        """
        Link variant to a product.

        :return: If linked successfully.
        """
        request = ProductVariantLinkAPI.get_request(product_id, product_variant_id)
        response = await self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductVariantLinkAPI.process_response(response)

    async def link_variant_to_products(self, product_ids_variant_ids: list[Tuple[str, str]]) -> list[bool]:
        """
        Link multiple variants to products.
        This NOT uses asyncio to make the requests concurrently, due to race condition on server side.

        :return: If linked successfully each.
        """
        return [
            await self.link_variant_to_product(product_id, product_variant_id)
            for product_id, product_variant_id in product_ids_variant_ids
        ]
