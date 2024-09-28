import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.get import GetResourceAPI
from plytix_pim_client.dtos.products.family import ProductFamily


class ProductFamilyGetAPI(GetResourceAPI):
    endpoint_prefix = "/api/v1/product_families"
    resource_dto_class = ProductFamily


class ProductFamilyGetAPISyncMixin(BaseAPISyncMixin):
    def get_family(self, product_family_id: str) -> ProductFamily | None:
        """
        Get a family.

        :return: The family.
        """
        request = ProductFamilyGetAPI.get_request(product_family_id)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductFamilyGetAPI.process_response(response)

    def get_families(self, product_family_ids: list[str]) -> list[ProductFamily | None]:
        """
        Get multiple families. This uses threading to make the requests concurrently.

        :return: The families.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.get_family, product_family_id) for product_family_id in product_family_ids]
            return [future.result() for future in futures]


class ProductFamilyGetAPIAsyncMixin(BaseAPIAsyncMixin):
    async def get_family(self, product_family_id: str) -> ProductFamily | None:
        """
        Get a family.

        :return: The family.
        """
        request = ProductFamilyGetAPI.get_request(product_family_id)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductFamilyGetAPI.process_response(response)

    async def get_families(self, product_family_ids: list[str]) -> list[ProductFamily | None]:
        """
        Get multiple families. This uses asyncio to make the requests concurrently.

        :return: The families.
        """
        return list(
            await asyncio.gather(*[self.get_family(product_family_id) for product_family_id in product_family_ids])
        )
