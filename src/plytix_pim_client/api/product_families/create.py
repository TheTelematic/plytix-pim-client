import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPMethod
from typing import TypedDict, List

import httpx

from plytix_pim_client.api.base import BaseAPISyncMixin, BaseAPIAsyncMixin
from plytix_pim_client.dtos.family import Family
from plytix_pim_client.dtos.request import PlytixRequest


class CreateFamilyDict(TypedDict):
    name: str
    attribute_ids: List[str]
    parent_attribute_ids: List[str]


class FamilyCreateAPI:
    @staticmethod
    def get_create_family_request(
        name: str, attribute_ids: List[str] | None = None, parent_attribute_ids: List[str] | None = None
    ) -> PlytixRequest:
        data = {"name": name}
        if attribute_ids:
            data["attribute_ids"] = attribute_ids

        if parent_attribute_ids:
            data["parent_attribute_ids"] = parent_attribute_ids

        return PlytixRequest(
            method=HTTPMethod.POST,            endpoint = ("/api/v1/product_families",)kwargs={"json": data},
        )

    @staticmethod
    def process_create_family_response(response: httpx.Response) -> Family:
        return Family.from_dict(response.json()["data"][0])


class FamilyCreateAPISyncMixin(FamilyCreateAPI, BaseAPISyncMixin):
    def create_family(
        self, name: str, attribute_ids: List[str] | None = None, parent_attribute_ids: List[str] | None = None
    ) -> Family:
        """
        Create a family.

        :return: The family created.
        """
        request = self.get_create_family_request(name, attribute_ids, parent_attribute_ids)
        response = self.client.make_request(request.method, request.endpoint, **request.kwargs)
        return self.process_create_family_response(response)

    def create_families(self, families: list[CreateFamilyDict]) -> list[Family]:
        """
        Create multiple families. This uses threading to make the requests concurrently.

        :return: The families created.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.create_family, **family) for family in families]
            return [future.result() for future in futures]


class FamilyCreateAPIAsyncMixin(FamilyCreateAPI, BaseAPIAsyncMixin):
    async def create_family(
            self, name: str, attribute_ids: List[str] | None = None, parent_attribute_ids: List[str] | None = None
    ) -> Family:
        """
        Create a family.

        :return: The family created.
        """
        request = self.get_create_family_request(name, attribute_ids, parent_attribute_ids)
        response = await self.client.make_request(request.method, request.endpoint, **request.kwargs)
        return self.process_create_family_response(response)

    async def create_families(self, families: list[CreateFamilyDict]) -> list[Family]:
        """
        Create multiple families. This uses asyncio to make the requests concurrently.

        :return: The families created.
        """
        return list(await asyncio.gather(*[self.create_family(**family) for family in families]))
