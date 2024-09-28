import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Dict, List, TypedDict

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.create import CreateResourceAPI
from plytix_pim_client.dtos.products.family import ProductFamily


class CreateProductFamilyDict(TypedDict):
    name: str
    attribute_ids: List[str]
    parent_attribute_ids: List[str]


class ProductFamilyCreateAPI(CreateResourceAPI):
    endpoint = "/api/v1/product_families"
    resource_dto_class = ProductFamily


class ProductFamilyCreateAPISyncMixin(BaseAPISyncMixin):
    def create_family(
        self, name: str, attribute_ids: List[str] | None = None, parent_attribute_ids: List[str] | None = None
    ) -> ProductFamily:
        """
        Create a family.

        :return: The family created.
        """
        data: Dict[str, str | List[str]] = {
            "name": name,
            "attribute_ids": attribute_ids or [],
            "parent_attribute_ids": parent_attribute_ids or [],
        }

        request = ProductFamilyCreateAPI.get_request(**data)
        response = self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductFamilyCreateAPI.process_response(response)

    def create_families(self, families: list[CreateProductFamilyDict]) -> list[ProductFamily]:
        """
        Create multiple families. This uses threading to make the requests concurrently.

        :return: The families created.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.create_family, **family) for family in families]
            return [future.result() for future in futures]


class ProductFamilyCreateAPIAsyncMixin(BaseAPIAsyncMixin):
    async def create_family(
        self, name: str, attribute_ids: List[str] | None = None, parent_attribute_ids: List[str] | None = None
    ) -> ProductFamily:
        """
        Create a family.

        :return: The family created.
        """
        data: Dict[str, str | List[str]] = {
            "name": name,
            "attribute_ids": attribute_ids or [],
            "parent_attribute_ids": parent_attribute_ids or [],
        }

        request = ProductFamilyCreateAPI.get_request(**data)
        response = await self._client.make_request(request.method, request.endpoint, **request.kwargs)
        return ProductFamilyCreateAPI.process_response(response)

    async def create_families(self, families: list[CreateProductFamilyDict]) -> list[ProductFamily]:
        """
        Create multiple families. This uses asyncio to make the requests concurrently.

        :return: The families created.
        """
        return list(await asyncio.gather(*[self.create_family(**family) for family in families]))
