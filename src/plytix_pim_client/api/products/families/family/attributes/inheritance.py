import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPMethod, HTTPStatus
from typing import List, Tuple

import httpx

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.request import PlytixRequest


class ProductFamilyEditAttributeInheritanceAPI:
    @staticmethod
    def get_request(
        product_family_id: str,
        attribute_labels_with_inheritance_on: List[str],
        attribute_labels_with_inheritance_off: List[str],
    ) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.POST,
            endpoint=f"api/v1/product_families/{product_family_id}/attributes/edit",
            kwargs={
                "json": {
                    "parent_level": [f"attributes.{label}" for label in attribute_labels_with_inheritance_on],
                    "no_level": [f"attributes.{label}" for label in attribute_labels_with_inheritance_off],
                }
            },
        )

    @staticmethod
    def process_response(response: httpx.Response) -> bool | None:
        if response.status_code in [
            HTTPStatus.NOT_FOUND,
        ]:
            return None

        return True


class ProductFamilyEditAttributeInheritanceAPISyncMixin(BaseAPISyncMixin):
    def edit_attributes_inheritance(
        self,
        product_family_id: str,
        attribute_labels_with_inheritance_on: List[str],
        attribute_labels_with_inheritance_off: List[str],
    ) -> bool | None:
        """
        Edit the inheritance of the given attributes in the given family.

        :return: If edited successfully.
        """
        request = ProductFamilyEditAttributeInheritanceAPI.get_request(
            product_family_id, attribute_labels_with_inheritance_on, attribute_labels_with_inheritance_off
        )
        response = self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductFamilyEditAttributeInheritanceAPI.process_response(response)

    def edit_attributes_inheritances(
        self, family_ids_with_attributes_ids_on_and_off: list[Tuple[str, List[str], List[str]]]
    ) -> list[bool | None]:
        """
        Edit the inheritance of the given attributes in the given families.
        This uses threading to make the requests concurrently.

        :return: If edited successfully each.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    self.edit_attributes_inheritance,
                    product_family_id,
                    attribute_labels_with_inheritance_on,
                    attribute_labels_with_inheritance_off,
                )
                for product_family_id, attribute_labels_with_inheritance_on, attribute_labels_with_inheritance_off
                in family_ids_with_attributes_ids_on_and_off  # fmt: skip
            ]
            return [future.result() for future in futures]


class ProductFamilyEditAttributeInheritanceAPIAsyncMixin(BaseAPIAsyncMixin):
    async def edit_attributes_inheritance(
        self,
        product_family_id: str,
        attribute_labels_with_inheritance_on: List[str],
        attribute_labels_with_inheritance_off: List[str],
    ) -> bool | None:
        """
        Edit the inheritance of the given attributes in the given family.

        :return: If edited successfully.
        """
        request = ProductFamilyEditAttributeInheritanceAPI.get_request(
            product_family_id, attribute_labels_with_inheritance_on, attribute_labels_with_inheritance_off
        )
        response = await self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductFamilyEditAttributeInheritanceAPI.process_response(response)

    async def edit_attributes_inheritances(
        self, family_ids_with_attributes_ids_on_and_off: list[Tuple[str, List[str], List[str]]]
    ) -> list[bool | None]:
        """
        Edit the inheritance of the given attributes in the given families.
        This uses asyncio to make the requests concurrently.

        :return: If edited successfully each.
        """
        return list(
            await asyncio.gather(
                *[
                    self.edit_attributes_inheritance(
                        product_family_id, attribute_labels_with_inheritance_on, attribute_labels_with_inheritance_off
                    )
                    for product_family_id, attribute_labels_with_inheritance_on, attribute_labels_with_inheritance_off
                    in family_ids_with_attributes_ids_on_and_off  # fmt: skip
                ]
            )
        )
