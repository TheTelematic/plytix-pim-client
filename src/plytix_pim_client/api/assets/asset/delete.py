import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.delete import DeleteResourceAPI


class AssetDeleteAPI(DeleteResourceAPI):
    endpoint_prefix = "/api/v1/assets"


class AssetDeleteAPISyncMixin(BaseAPISyncMixin):
    def delete_asset(self, asset_id: str) -> bool:
        """
        Delete an asset.

        :return: True if deleted, False if it didn't exist.
        """
        request = AssetDeleteAPI.get_request(asset_id)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return AssetDeleteAPI.process_response(response)

    def delete_assets(self, asset_ids: list[str]) -> list[bool]:
        """
        Delete multiple assets. This uses threading to make the requests concurrently.

        :return: List of boolean. True if deleted, False if it didn't exist.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.delete_asset, asset_id) for asset_id in asset_ids]
            return [future.result() for future in futures]


class AssetDeleteAPIAsyncMixin(BaseAPIAsyncMixin):
    async def delete_asset(self, asset_id: str) -> bool:
        """
        Delete an asset.

        :return: True if deleted, False if it didn't exist.
        """
        request = AssetDeleteAPI.get_request(asset_id)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return AssetDeleteAPI.process_response(response)

    async def delete_assets(self, asset_ids: list[str]) -> list[bool]:
        """
        Delete multiple assets. This uses asyncio to make the requests concurrently.

        :return: List of boolean. True if deleted, False if it didn't exist.
        """
        return list(await asyncio.gather(*[self.delete_asset(asset_id) for asset_id in asset_ids]))
