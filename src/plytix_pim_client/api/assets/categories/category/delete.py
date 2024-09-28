import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.delete import DeleteResourceAPI


class AssetCategoryDeleteAPI(DeleteResourceAPI):
    endpoint_prefix = "/api/v1/categories/file"


class AssetCategoryDeleteAPISyncMixin(BaseAPISyncMixin):
    def delete_asset_category(self, category_id: str) -> bool:
        """
        Delete an asset category.

        :return: True if deleted, False if it didn't exist.
        """
        request = AssetCategoryDeleteAPI.get_request(category_id)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return AssetCategoryDeleteAPI.process_response(response)

    def delete_asset_categories(self, category_ids: list[str]) -> list[bool]:
        """
        Delete multiple asset categories. This uses threading to make the requests concurrently.

        :return: List of boolean. True if deleted, False if it didn't exist.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.delete_asset_category, category_id) for category_id in category_ids]
            return [future.result() for future in futures]


class AssetCategoryDeleteAPIAsyncMixin(BaseAPIAsyncMixin):
    async def delete_asset_category(self, category_id: str) -> bool:
        """
        Delete an asset category.

        :return: True if deleted, False if it didn't exist.
        """
        request = AssetCategoryDeleteAPI.get_request(category_id)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return AssetCategoryDeleteAPI.process_response(response)

    async def delete_asset_categories(self, category_ids: list[str]) -> list[bool]:
        """
        Delete multiple asset categories. This uses asyncio to make the requests concurrently.

        :return: List of boolean. True if deleted, False if it didn't exist.
        """
        return list(await asyncio.gather(*[self.delete_asset_category(category_id) for category_id in category_ids]))
