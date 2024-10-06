from http import HTTPMethod, HTTPStatus
from typing import Tuple

import httpx

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.request import PlytixRequest


class ProductVariantUnlinkAPI:
    @staticmethod
    def get_request(
        product_id: str,
        product_variant_id: str,
    ) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.DELETE,
            endpoint=f"api/v1/products/{product_id}/variant/{product_variant_id}",
        )

    @staticmethod
    def process_response(response: httpx.Response) -> bool:
        if response.status_code in [
            HTTPStatus.NOT_FOUND,
        ]:
            return False

        return True


class ProductVariantUnlinkAPISyncMixin(BaseAPISyncMixin):
    def unlink_variant_from_product(
        self,
        product_id: str,
        product_variant_id: str,
    ) -> bool:
        """
        Unlink variant to a product.

        :return: If unlinked successfully.
        """
        request = ProductVariantUnlinkAPI.get_request(product_id, product_variant_id)
        response = self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductVariantUnlinkAPI.process_response(response)

    def unlink_variant_from_products(self, product_ids_variant_ids: list[Tuple[str, str]]) -> list[bool]:
        """
        Unlink multiple variants to products.
        This NOT uses threading to make the requests concurrently, due to race condition on server side.

        :return: If unlinked successfully each.
        """
        return [
            self.unlink_variant_from_product(product_id, product_variant_id)
            for product_id, product_variant_id in product_ids_variant_ids
        ]


class ProductVariantUnlinkAPIAsyncMixin(BaseAPIAsyncMixin):
    async def unlink_variant_from_product(
        self,
        product_id: str,
        product_variant_id: str,
    ) -> bool:
        """
        Unlink variant to a product.

        :return: If unlinked successfully.
        """
        request = ProductVariantUnlinkAPI.get_request(product_id, product_variant_id)
        response = await self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductVariantUnlinkAPI.process_response(response)

    async def unlink_variant_from_products(self, product_ids_variant_ids: list[Tuple[str, str]]) -> list[bool]:
        """
        Unlink multiple variants to products.
        This NOT uses asyncio to make the requests concurrently, due to race condition on server side.

        :return: If unlinked successfully each.
        """
        return [
            await self.unlink_variant_from_product(product_id, product_variant_id)
            for product_id, product_variant_id in product_ids_variant_ids
        ]
