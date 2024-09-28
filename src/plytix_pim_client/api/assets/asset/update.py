import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus
from typing import Dict, Tuple

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.update import UpdateResourceAPI
from plytix_pim_client.dtos.assets.asset import Asset


class AssetUpdateAPI(UpdateResourceAPI):
    endpoint_prefix = "/api/v1/assets"
    resource_dto_class = Asset


class AssetUpdateAPISyncMixin(BaseAPISyncMixin):
    def update_asset(
        self,
        asset_id: str,
        filename: str | None = None,
        public: bool | None = None,
        category_ids: list[str] | None = None,
    ) -> Asset | None:
        """
        Update an asset.

        :return: The asset.
        """
        data: Dict[str, str | bool | list[str]] = {}
        if filename:
            data["filename"] = filename
        if public:
            data["public"] = public
        if category_ids:
            data["categories"] = category_ids

        request = AssetUpdateAPI.get_request(asset_id, data)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return AssetUpdateAPI.process_response(response)

    def update_assets(self, asset_ids_and_data: list[Tuple[str, dict]]) -> list[Asset | None]:
        """
        Update multiple assets. This uses threading to make the requests concurrently.

        :return: The assets.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.update_asset, asset_id, **data) for asset_id, data in asset_ids_and_data]
            return [future.result() for future in futures]


class AssetUpdateAPIAsyncMixin(BaseAPIAsyncMixin):
    async def update_asset(
        self,
        asset_id: str,
        filename: str | None = None,
        public: bool | None = None,
        category_ids: list[str] | None = None,
    ) -> Asset | None:
        """
        Update an asset.

        :return: The asset.
        """
        data: Dict[str, str | bool | list[str]] = {}
        if filename:
            data["filename"] = filename
        if public:
            data["public"] = public
        if category_ids:
            data["categories"] = category_ids

        request = AssetUpdateAPI.get_request(asset_id, data)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return AssetUpdateAPI.process_response(response)

    async def update_assets(self, asset_ids_and_data: list[Tuple[str, dict]]) -> list[Asset | None]:
        """
        Update multiple assets. This uses asyncio to make the requests concurrently.

        :return: The assets.
        """
        return list(
            await asyncio.gather(*[self.update_asset(asset_id, **data) for asset_id, data in asset_ids_and_data])
        )
