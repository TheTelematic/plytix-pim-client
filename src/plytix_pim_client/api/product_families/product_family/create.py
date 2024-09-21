import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from typing import TypedDict, List, Dict

from plytix_pim_client.api.base import BaseAPISyncMixin, BaseAPIAsyncMixin
from plytix_pim_client.api.common.create import CreateResourceAPI
from plytix_pim_client.dtos.family import Family


class CreateFamilyDict(TypedDict):
    name: str
    attribute_ids: List[str]
    parent_attribute_ids: List[str]


class FamilyCreateAPI(CreateResourceAPI):
    endpoint = "/api/v1/product_families"
    resource_dto_class = Family


class FamilyCreateAPISyncMixin(BaseAPISyncMixin):
    def create_family(
        self, name: str, attribute_ids: List[str] | None = None, parent_attribute_ids: List[str] | None = None
    ) -> Family:
        """
        Create a family.

        :return: The family created.
        """
        data: Dict[str, str | List[str]] = {
            "name": name,
            "attribute_ids": attribute_ids or [],
            "parent_attribute_ids": parent_attribute_ids or [],
        }

        request = FamilyCreateAPI.get_request(**data)
        response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return FamilyCreateAPI.process_response(response)

    def create_families(self, families: list[CreateFamilyDict]) -> list[Family]:
        """
        Create multiple families. This uses threading to make the requests concurrently.

        :return: The families created.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.create_family, **family) for family in families]
            return [future.result() for future in futures]


class FamilyCreateAPIAsyncMixin(BaseAPIAsyncMixin):
    async def create_family(
        self, name: str, attribute_ids: List[str] | None = None, parent_attribute_ids: List[str] | None = None
    ) -> Family:
        """
        Create a family.

        :return: The family created.
        """
        data: Dict[str, str | List[str]] = {
            "name": name,
            "attribute_ids": attribute_ids or [],
            "parent_attribute_ids": parent_attribute_ids or [],
        }

        request = FamilyCreateAPI.get_request(**data)
        response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return FamilyCreateAPI.process_response(response)

    async def create_families(self, families: list[CreateFamilyDict]) -> list[Family]:
        """
        Create multiple families. This uses asyncio to make the requests concurrently.

        :return: The families created.
        """
        return list(await asyncio.gather(*[self.create_family(**family) for family in families]))
