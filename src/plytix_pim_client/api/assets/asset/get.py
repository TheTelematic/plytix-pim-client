import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.get import GetResourceAPI
from plytix_pim_client.dtos.assets.asset import Asset


class AssetGetAPI(GetResourceAPI):
    endpoint_prefix = "/api/v1/assets"
    resource_dto_class = Asset


class AssetGetAPISyncMixin(BaseAPISyncMixin):
    def get_asset(self, asset_id: str) -> Asset | None:
        """
        Get an asset.

        :return: The asset.
        """
        request = AssetGetAPI.get_request(asset_id)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return AssetGetAPI.process_response(response)

    def get_assets(self, asset_ids: list[str]) -> list[Asset | None]:
        """
        Get multiple assets. This uses threading to make the requests concurrently.

        :return: The assets.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.get_asset, asset_id) for asset_id in asset_ids]
            return [future.result() for future in futures]


class AssetGetAPIAsyncMixin(BaseAPIAsyncMixin):
    async def get_asset(self, asset_id: str) -> Asset | None:
        """
        Get an asset.

        :return: The asset.
        """
        request = AssetGetAPI.get_request(asset_id)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return AssetGetAPI.process_response(response)

    async def get_assets(self, asset_ids: list[str]) -> list[Asset | None]:
        """
        Get multiple assets. This uses asyncio to make the requests concurrently.

        :return: The assets.
        """
        return list(await asyncio.gather(*[self.get_asset(asset_id) for asset_id in asset_ids]))
