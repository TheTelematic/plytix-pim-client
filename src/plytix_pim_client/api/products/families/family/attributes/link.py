import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPMethod, HTTPStatus
from typing import Tuple, List

import httpx

from plytix_pim_client.api.base import BaseAPISyncMixin, BaseAPIAsyncMixin
from plytix_pim_client.dtos.family import AttributeLevel
from plytix_pim_client.dtos.request import PlytixRequest


class ProductFamilyLinkAttributeAPI:
    @staticmethod
    def get_request(
        product_family_id: str, attribute_ids: List[str], attributes_level: AttributeLevel = AttributeLevel.OFF
    ) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.POST,
            endpoint=f"api/v1/product_families/{product_family_id}/attributes/link",
            kwargs={"json": {"attributes": attribute_ids, "attributes_level": attributes_level}},
        )

    @staticmethod
    def process_response(response: httpx.Response) -> bool | None:
        if response.status_code in [
            HTTPStatus.NOT_FOUND,
        ]:
            return None

        return True


class ProductFamilyLinkAttributeAPISyncMixin(BaseAPISyncMixin):
    def link_attribute_to_family(
        self, product_family_id: str, attribute_ids: List[str], attributes_level: AttributeLevel = AttributeLevel.OFF
    ) -> bool | None:
        """
        Assign a family to product.

        :return: The product.
        """
        request = ProductFamilyLinkAttributeAPI.get_request(product_family_id, attribute_ids, attributes_level)
        response = self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductFamilyLinkAttributeAPI.process_response(response)

    def link_attributes_to_families(
        self, family_ids_with_attributes_and_level: list[Tuple[str, List[str], AttributeLevel]]
    ) -> list[bool | None]:
        """
        Assign a family to multiple products. This uses threading to make the requests concurrently.

        :return: The products.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.link_attribute_to_family, product_family_id, attribute_ids, attributes_level)
                for product_family_id, attribute_ids, attributes_level in family_ids_with_attributes_and_level
            ]
            return [future.result() for future in futures]


class ProductFamilyLinkAttributeAPIAsyncMixin(BaseAPIAsyncMixin):
    async def link_attribute_to_family(
        self, product_family_id: str, attribute_ids: List[str], attributes_level: AttributeLevel = AttributeLevel.OFF
    ) -> bool | None:
        """
        Assign a family to a product.

        :return: The product.
        """
        request = ProductFamilyLinkAttributeAPI.get_request(product_family_id, attribute_ids, attributes_level)
        response = await self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductFamilyLinkAttributeAPI.process_response(response)

    async def link_attributes_to_families(
        self, family_ids_with_attributes_and_level: list[Tuple[str, List[str], AttributeLevel]]
    ) -> list[bool | None]:
        """
        Assign a family to multiple products. This uses asyncio to make the requests concurrently.

        :return: The products.
        """
        return list(
            await asyncio.gather(
                *[
                    self.link_attribute_to_family(product_family_id, attribute_ids, attributes_level)
                    for product_family_id, attribute_ids, attributes_level in family_ids_with_attributes_and_level
                ]
            )
        )
