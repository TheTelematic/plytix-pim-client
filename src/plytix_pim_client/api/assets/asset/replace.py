import asyncio
import os
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPMethod, HTTPStatus
from typing import IO, Tuple

import httpx

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.assets.asset import Asset
from plytix_pim_client.dtos.request import PlytixRequest


class AssetReplaceAPI:
    @classmethod
    def get_request(cls, resource_id: str, filename: str, file_obj: IO) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.PUT,
            endpoint=f"/api/v1/assets/{resource_id}/content",
            kwargs={"files": {"file": (filename, file_obj)}},
        )

    @classmethod
    def process_response(cls, response: httpx.Response) -> Asset | None:
        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        return Asset.from_dict(response.json()["data"][0])


class AssetReplaceAPISyncMixin(BaseAPISyncMixin):
    def replace_asset(
        self,
        asset_id: str,
        file_path: str,
    ) -> Asset | None:
        """
        Replace an asset content.

        :return: The asset.
        """
        filename = os.path.basename(file_path)

        with open(file_path, "rb") as file_obj:
            request = AssetReplaceAPI.get_request(asset_id, filename, file_obj)
            response = self._client.make_request(
                request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
            )
        return AssetReplaceAPI.process_response(response)

    def replace_assets(self, asset_ids_and_file_paths: list[Tuple[str, str]]) -> list[Asset | None]:
        """
        Replace multiple assets. This uses threading to make the requests concurrently.

        :return: The assets.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.replace_asset, asset_id, file_path)
                for asset_id, file_path in asset_ids_and_file_paths
            ]
            return [future.result() for future in futures]


class AssetReplaceAPIAsyncMixin(BaseAPIAsyncMixin):
    async def replace_asset(
        self,
        asset_id: str,
        file_path: str,
    ) -> Asset | None:
        """
        Replace an asset content.

        :return: The asset.
        """
        filename = os.path.basename(file_path)

        with open(file_path, "rb") as file_obj:
            request = AssetReplaceAPI.get_request(asset_id, filename, file_obj)
            response = await self._client.make_request(
                request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
            )

        return AssetReplaceAPI.process_response(response)

    async def replace_assets(self, asset_ids_and_file_paths: list[Tuple[str, str]]) -> list[Asset | None]:
        """
        Replace multiple assets. This uses asyncio to make the requests concurrently.

        :return: The assets.
        """
        return list(
            await asyncio.gather(
                *[self.replace_asset(asset_id, file_path) for asset_id, file_path in asset_ids_and_file_paths]
            )
        )
