from http import HTTPMethod, HTTPStatus
from typing import Tuple

import httpx

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.request import PlytixRequest


class ProductAssetLinkAPI:
    @staticmethod
    def get_request(
        product_id: str,
        product_asset_id: str,
        product_attribute_label: str,
    ) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.POST,
            endpoint=f"api/v1/products/{product_id}/assets",
            kwargs={"json": {"id": product_asset_id, "attribute_label": product_attribute_label}},
        )

    @staticmethod
    def process_response(response: httpx.Response) -> bool:
        if response.status_code in [
            HTTPStatus.NOT_FOUND,
        ]:
            return False

        return True


class ProductAssetLinkAPISyncMixin(BaseAPISyncMixin):
    def link_asset_to_product(
        self,
        product_id: str,
        product_asset_id: str,
        product_attribute_label: str,
    ) -> bool:
        """
        Link asset to a product.

        :return: If linked successfully.
        """
        request = ProductAssetLinkAPI.get_request(product_id, product_asset_id, product_attribute_label)
        response = self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductAssetLinkAPI.process_response(response)

    def link_asset_to_products(
        self, product_ids_asset_ids_and_attribute_labels: list[Tuple[str, str, str]]
    ) -> list[bool]:
        """
        Link multiple assets to products.
        This NOT uses threading to make the requests concurrently, due to race condition on server side.

        :return: If linked successfully each.
        """
        return [
            self.link_asset_to_product(product_id, product_asset_id, product_attribute_label)
            for product_id, product_asset_id, product_attribute_label in product_ids_asset_ids_and_attribute_labels
        ]


class ProductAssetLinkAPIAsyncMixin(BaseAPIAsyncMixin):
    async def link_asset_to_product(
        self,
        product_id: str,
        product_asset_id: str,
        product_attribute_label: str,
    ) -> bool:
        """
        Link asset to a product.

        :return: If linked successfully.
        """
        request = ProductAssetLinkAPI.get_request(product_id, product_asset_id, product_attribute_label)
        response = await self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductAssetLinkAPI.process_response(response)

    async def link_asset_to_products(
        self, product_ids_asset_ids_and_attribute_labels: list[Tuple[str, str, str]]
    ) -> list[bool]:
        """
        Link multiple assets to products.
        This NOT uses asyncio to make the requests concurrently, due to race condition on server side.

        :return: If linked successfully each.
        """
        return [
            await self.link_asset_to_product(product_id, product_asset_id, product_attribute_label)
            for product_id, product_asset_id, product_attribute_label in product_ids_asset_ids_and_attribute_labels
        ]
