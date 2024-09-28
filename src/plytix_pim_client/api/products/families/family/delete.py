import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.delete import DeleteResourceAPI


class ProductFamilyDeleteAPI(DeleteResourceAPI):
    endpoint_prefix = "/api/v1/product_families"


class ProductFamilyDeleteAPISyncMixin(BaseAPISyncMixin):
    def delete_family(self, product_family_id: str) -> bool:
        """
        Delete a family.

        :return: True if deleted, False if it didn't exist.
        """
        request = ProductFamilyDeleteAPI.get_request(product_family_id)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductFamilyDeleteAPI.process_response(response)

    def delete_families(self, product_family_ids: list[str]) -> list[bool]:
        """
        Delete multiple families. This uses threading to make the requests concurrently.

        :return: List of boolean. True if deleted, False if it didn't exist.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.delete_family, product_family_id) for product_family_id in product_family_ids
            ]
            return [future.result() for future in futures]


class ProductFamilyDeleteAPIAsyncMixin(BaseAPIAsyncMixin):
    async def delete_family(self, product_family_id: str) -> bool:
        """
        Delete a family.

        :return: True if deleted, False if it didn't exist.
        """
        request = ProductFamilyDeleteAPI.get_request(product_family_id)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductFamilyDeleteAPI.process_response(response)

    async def delete_families(self, product_family_ids: list[str]) -> list[bool]:
        """
        Delete multiple families. This uses asyncio to make the requests concurrently.

        :return: List of boolean. True if deleted, False if it didn't exist.
        """
        return list(
            await asyncio.gather(*[self.delete_family(product_family_id) for product_family_id in product_family_ids])
        )
