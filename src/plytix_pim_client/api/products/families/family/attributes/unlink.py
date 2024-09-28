import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPMethod, HTTPStatus
from typing import List, Tuple

import httpx

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.request import PlytixRequest


class ProductFamilyUnlinkAttributeAPI:
    @staticmethod
    def get_request(
        product_family_id: str,
        attribute_ids: List[str],
    ) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.POST,
            endpoint=f"api/v1/product_families/{product_family_id}/attributes/unlink",
            kwargs={"json": {"attributes": attribute_ids}},
        )

    @staticmethod
    def process_response(response: httpx.Response) -> bool | None:
        if response.status_code in [
            HTTPStatus.NOT_FOUND,
        ]:
            return None

        return True


class ProductFamilyUnlinkAttributeAPISyncMixin(BaseAPISyncMixin):
    def unlink_attribute_to_family(
        self,
        product_family_id: str,
        attribute_ids: List[str],
    ) -> bool | None:
        """
        Unlink attributes to family.

        :return: If linked successfully.
        """
        request = ProductFamilyUnlinkAttributeAPI.get_request(product_family_id, attribute_ids)
        response = self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductFamilyUnlinkAttributeAPI.process_response(response)

    def unlink_attributes_to_families(
        self, family_ids_with_attributes: list[Tuple[str, List[str]]]
    ) -> list[bool | None]:
        """
        Unlink attributes to multiple families. This uses threading to make the requests concurrently.

        :return: If linked successfully each.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.unlink_attribute_to_family, product_family_id, attribute_ids)
                for product_family_id, attribute_ids in family_ids_with_attributes
            ]
            return [future.result() for future in futures]


class ProductFamilyUnlinkAttributeAPIAsyncMixin(BaseAPIAsyncMixin):
    async def unlink_attribute_to_family(
        self,
        product_family_id: str,
        attribute_ids: List[str],
    ) -> bool | None:
        """
        Unlink attributes to family.

        :return: If linked successfully.
        """
        request = ProductFamilyUnlinkAttributeAPI.get_request(product_family_id, attribute_ids)
        response = await self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductFamilyUnlinkAttributeAPI.process_response(response)

    async def unlink_attributes_to_families(
        self, family_ids_with_attributes: list[Tuple[str, List[str]]]
    ) -> list[bool | None]:
        """
        Unlink attributes to multiple families. This uses asyncio to make the requests concurrently.

        :return: If linked successfully each.
        """
        return list(
            await asyncio.gather(
                *[
                    self.unlink_attribute_to_family(product_family_id, attribute_ids)
                    for product_family_id, attribute_ids in family_ids_with_attributes
                ]
            )
        )
