import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPMethod
from typing import TypedDict

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.create import CreateResourceAPI
from plytix_pim_client.dtos.assets.category import AssetCategory
from plytix_pim_client.dtos.request import PlytixRequest


class CreateAssetCategoryDict(TypedDict):
    name: str
    parent_category_id: str | None


class AssetCategoryCreateAPI(CreateResourceAPI):
    endpoint = "/api/v1/categories/file"
    resource_dto_class = AssetCategory

    @classmethod
    def get_request(cls, **data) -> PlytixRequest:
        if data.get("parent_category_id"):
            endpoint = f"{cls.endpoint}/{data['parent_category_id']}"
        else:
            endpoint = cls.endpoint

        return PlytixRequest(
            method=HTTPMethod.POST,
            endpoint=endpoint,
            kwargs={"json": {"name": data["name"]}},
        )


class AssetCategoryCreateAPISyncMixin(BaseAPISyncMixin):
    def create_asset_category(self, name: str, parent_category_id: str | None = None) -> AssetCategory:
        """
        Create an asset category.

        :return: The asset category created.
        """
        request = AssetCategoryCreateAPI.get_request(name=name, parent_category_id=parent_category_id)
        response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return AssetCategoryCreateAPI.process_response(response)

    def create_asset_categories(self, asset_categories: list[CreateAssetCategoryDict]) -> list[AssetCategory]:
        """
        Create multiple asset categories. This uses threading to make the requests concurrently.

        :return: The asset categories created.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.create_asset_category, **category) for category in asset_categories]
            return [future.result() for future in futures]


class AssetCategoryCreateAPIAsyncMixin(BaseAPIAsyncMixin):
    async def create_asset_category(self, name: str, parent_category_id: str | None = None) -> AssetCategory:
        """
        Create an asset category.

        :return: The asset category created.
        """
        request = AssetCategoryCreateAPI.get_request(name=name, parent_category_id=parent_category_id)
        response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return AssetCategoryCreateAPI.process_response(response)

    async def create_asset_categories(self, asset_categories: list[CreateAssetCategoryDict]) -> list[AssetCategory]:
        """
        Create multiple asset categories. This uses asyncio to make the requests concurrently.

        :return: The asset categories created.
        """
        return list(await asyncio.gather(*[self.create_asset_category(**category) for category in asset_categories]))
