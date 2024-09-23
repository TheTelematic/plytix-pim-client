import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from typing import TypedDict

from plytix_pim_client.api.base import BaseAPISyncMixin, BaseAPIAsyncMixin
from plytix_pim_client.api.common.create import CreateResourceAPI
from plytix_pim_client.dtos.asset import Asset


class CreateAssetFromURLDict(TypedDict):
    url: str
    filename: str | None


# TODO: To fix in #26
# class CreateAssetFromLocalFileDict(TypedDict):
#     file_path: str


class AssetCreateAPI(CreateResourceAPI):
    endpoint = "/api/v1/assets"
    resource_dto_class = Asset


class AssetCreateAPISyncMixin(BaseAPISyncMixin):
    def create_asset_by_url(self, url: str, filename: str | None = None) -> Asset:
        """
        Create an asset using a public URL.

        :return: The asset created.
        """
        data = {"url": url}
        if filename:
            data["filename"] = filename

        request = AssetCreateAPI.get_request(**data)
        response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return AssetCreateAPI.process_response(response)

    # TODO: To fix in #26
    # def create_asset_from_local_file(self, file_path: str) -> Asset:
    #     """
    #     Create an asset uploading a local file.
    #
    #     :return: The asset created.
    #     """
    #     filename = os.path.basename(file_path)
    #     with open(file_path, "rb") as file_obj:
    #         content = base64.encodebytes(file_obj.read()).decode()
    #
    #     request = AssetCreateAPI.get_request(content=content, filename=filename)
    #     response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
    #     return AssetCreateAPI.process_response(response)

    def create_assets_by_urls(self, assets: list[CreateAssetFromURLDict]) -> list[Asset]:
        """
        Create multiple assets using public URLs. This uses threading to make the requests concurrently.

        :return: The assets created.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.create_asset_by_url, **asset) for asset in assets]
            return [future.result() for future in futures]

    # TODO: To fix in #26
    # def create_assets_from_local_files(self, assets: list[CreateAssetFromLocalFileDict]) -> list[Asset]:
    #     """
    #     Create multiple assets uploading local files. This uses threading to make the requests concurrently.
    #
    #     :return: The assets created.
    #     """
    #     with ThreadPoolExecutor() as executor:
    #         futures = [executor.submit(self.create_asset_by_url, **asset) for asset in assets]
    #         return [future.result() for future in futures]


class AssetCreateAPIAsyncMixin(BaseAPIAsyncMixin):
    async def create_asset_by_url(self, url: str, filename: str | None = None) -> Asset:
        """
        Create an asset using a public URL.

        :return: The asset created.
        """
        data = {"url": url}
        if filename:
            data["filename"] = filename

        request = AssetCreateAPI.get_request(**data)
        response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return AssetCreateAPI.process_response(response)

    # TODO: To fix in #26
    # async def create_asset_from_local_file(self, file_path: str) -> Asset:
    #     """
    #     Create an asset uploading a local file.
    #
    #     :return: The asset created.
    #     """
    #     filename = os.path.basename(file_path)
    #     async with aiofiles.open(file_path, "rb") as file_obj:
    #         content = base64.encodebytes(await file_obj.read()).decode()
    #
    #     request = AssetCreateAPI.get_request(content=content, filename=filename)
    #     response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
    #     return AssetCreateAPI.process_response(response)

    async def create_assets_by_urls(self, assets: list[CreateAssetFromURLDict]) -> list[Asset]:
        """
        Create multiple assets using public URLs. This uses asyncio to make the requests concurrently.

        :return: The assets created.
        """
        return list(await asyncio.gather(*[self.create_asset_by_url(**asset) for asset in assets]))

    # TODO: To fix in #26
    # async def create_assets_from_local_files(self, assets: list[CreateAssetFromURLDict]) -> list[Asset]:
    #     """
    #     Create multiple assets uploading local files. This uses asyncio to make the requests concurrently.
    #
    #     :return: The assets created.
    #     """
    #     return list(await asyncio.gather(*[self.create_asset_by_url(**asset) for asset in assets]))