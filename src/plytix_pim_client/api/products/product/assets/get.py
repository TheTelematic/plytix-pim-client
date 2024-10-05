import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus, HTTPMethod
from typing import Tuple, List

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.products.asset import ProductAsset
from plytix_pim_client.dtos.request import PlytixRequest


class ProductAssetsGetAPI:
    @classmethod
    def get_request(cls, **data) -> PlytixRequest:
        if data.get("product_asset_id"):
            endpoint = f"/api/v1/products/{data['product_id']}/assets/{data['product_asset_id']}"
        else:
            endpoint = f"/api/v1/products/{data['product_id']}/assets"

        return PlytixRequest(
            method=HTTPMethod.GET,
            endpoint=endpoint,
        )

    @classmethod
    def process_response(cls, response) -> List[ProductAsset] | None:
        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        if data := response.json().get("data", []):
            return [ProductAsset.from_dict(item) for item in data]

        return []


class ProductAssetsGetAPISyncMixin(BaseAPISyncMixin):
    def get_product_assets(self, product_id: str, product_asset_id: str | None = None) -> List[ProductAsset] | None:
        """
        Get a product asset if given, otherwise, all are returned.

        :return: The product assets.
        """
        request = ProductAssetsGetAPI.get_request(product_id=product_id, product_asset_id=product_asset_id)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductAssetsGetAPI.process_response(response)

    def get_multiple_product_assets(
        self, product_ids_and_asset_ids: list[Tuple[str, str | None]]
    ) -> List[List[ProductAsset] | None]:
        """
        Get the assets for multiple products. This uses threading to make the requests concurrently.

        :return: The product assets.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.get_product_assets, product_id, product_asset_id)
                for product_id, product_asset_id in product_ids_and_asset_ids
            ]
            return [future.result() for future in futures]


class ProductAssetsGetAPIAsyncMixin(BaseAPIAsyncMixin):
    async def get_product_assets(
        self, product_id: str, product_asset_id: str | None = None
    ) -> List[ProductAsset] | None:
        """
        Get a product asset if given, otherwise, all are returned.

        :return: The product assets.
        """
        request = ProductAssetsGetAPI.get_request(product_id=product_id, product_asset_id=product_asset_id)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductAssetsGetAPI.process_response(response)

    async def get_multiple_product_assets(
        self, product_ids_and_asset_ids: list[Tuple[str, str | None]]
    ) -> List[List[ProductAsset] | None]:
        """
        Get the assets for multiple products. This uses threading to make the requests concurrently.

        :return: The product assets.
        """
        return list(
            await asyncio.gather(
                *[
                    self.get_product_assets(product_id, product_asset_id)
                    for product_id, product_asset_id in product_ids_and_asset_ids
                ]
            )
        )
