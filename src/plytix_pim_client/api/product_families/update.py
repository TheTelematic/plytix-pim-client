import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus

from plytix_pim_client.api.base import BaseAPISyncMixin, BaseAPIAsyncMixin
from plytix_pim_client.api.common.update import UpdateResourceAPI
from plytix_pim_client.dtos.family import Family


class FamilyUpdateAPI(UpdateResourceAPI):
    endpoint_prefix = "/api/v1/product_families"
    resource_dto_class = Family


class FamilyUpdateAPISyncMixin(BaseAPISyncMixin):
    def rename_family(self, product_family_id: str, new_name: str) -> Family | None:
        """
        Update a family.

        :return: The family.
        """
        request = FamilyUpdateAPI.get_request(product_family_id, {"name": new_name})
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return FamilyUpdateAPI.process_response(response)

    def rename_families(self, product_family_ids: list[str]) -> list[Family | None]:
        """
        Update multiple families. This uses threading to make the requests concurrently.

        :return: The families.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.rename_family, product_family_id) for product_family_id in product_family_ids
            ]
            return [future.result() for future in futures]


class FamilyUpdateAPIAsyncMixin(BaseAPIAsyncMixin):
    async def rename_family(self, product_family_id: str, new_name: str) -> Family | None:
        """
        Update a family.

        :return: The family.
        """
        request = FamilyUpdateAPI.get_request(product_family_id, {"name": new_name})
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return FamilyUpdateAPI.process_response(response)

    async def rename_families(self, product_family_ids: list[str]) -> list[Family | None]:
        """
        Update multiple families. This uses asyncio to make the requests concurrently.

        :return: The families.
        """
        return list(
            await asyncio.gather(*[self.rename_family(product_family_id) for product_family_id in product_family_ids])
        )
