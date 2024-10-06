import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPMethod, HTTPStatus
from typing import Tuple

import httpx

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.request import PlytixRequest


class ProductAssetUnlinkAPI:
    @staticmethod
    def get_request(
        product_id: str,
        product_asset_id: str,
    ) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.DELETE,
            endpoint=f"api/v1/products/{product_id}/assets/{product_asset_id}",
        )

    @staticmethod
    def process_response(response: httpx.Response) -> bool:
        if response.status_code in [
            HTTPStatus.NOT_FOUND,
        ]:
            return False

        return True


class ProductAssetUnlinkAPISyncMixin(BaseAPISyncMixin):
    def unlink_asset_from_product(
        self,
        product_id: str,
        product_asset_id: str,
    ) -> bool:
        """
        Unlink asset from product.

        :return: If unlinked successfully.
        """
        request = ProductAssetUnlinkAPI.get_request(product_id, product_asset_id)
        response = self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductAssetUnlinkAPI.process_response(response)

    def unlink_asset_from_products(self, product_ids_and_asset_ids: list[Tuple[str, str]]) -> list[bool]:
        """
        Unlink multiple assets from products. This uses threading to make the requests concurrently.

        :return: If unlinked successfully each.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.unlink_asset_from_product, product_id, product_asset_id)
                for product_id, product_asset_id in product_ids_and_asset_ids
            ]
            return [future.result() for future in futures]


class ProductAssetUnlinkAPIAsyncMixin(BaseAPIAsyncMixin):
    async def unlink_asset_from_product(
        self,
        product_id: str,
        product_asset_id: str,
    ) -> bool:
        """
        Unlink asset from product.

        :return: If unlinked successfully.
        """
        request = ProductAssetUnlinkAPI.get_request(product_id, product_asset_id)
        response = await self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductAssetUnlinkAPI.process_response(response)

    async def unlink_asset_from_products(self, product_ids_and_asset_ids: list[Tuple[str, str]]) -> list[bool]:
        """
        Unlink multiple assets from products. This uses asyncio to make the requests concurrently.

        :return: If unlinked successfully each.
        """
        return list(
            await asyncio.gather(
                *[
                    self.unlink_asset_from_product(product_id, product_asset_id)
                    for product_id, product_asset_id in product_ids_and_asset_ids
                ]
            )
        )
