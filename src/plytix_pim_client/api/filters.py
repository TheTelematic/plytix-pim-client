from http import HTTPStatus
from typing import List

import httpx

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.get import GetResourceAPI
from plytix_pim_client.dtos.filters import AvailableSearchFilter


class FiltersGetAPI(GetResourceAPI):
    endpoint_prefix = "/api/v1/filters"
    resource_dto_class = AvailableSearchFilter

    @classmethod
    def process_response(cls, response: httpx.Response) -> List[AvailableSearchFilter]:
        json_response = response.json()
        filters = json_response["data"][0].get("attributes", []) + json_response["data"][0].get("properties", [])
        return [cls.resource_dto_class.from_dict(f) for f in filters]


class FiltersGetAPISyncMixin(BaseAPISyncMixin):
    def get_assets_filters(self) -> List[AvailableSearchFilter]:
        """
        Get all available filters for assets.

        :return: The available filters.
        """
        request = FiltersGetAPI.get_request("asset")
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return FiltersGetAPI.process_response(response)

    def get_products_filters(self) -> List[AvailableSearchFilter]:
        """
        Get all available filters for products.

        :return: The available filters.
        """
        request = FiltersGetAPI.get_request("product")
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return FiltersGetAPI.process_response(response)

    def get_relationships_filters(self) -> List[AvailableSearchFilter]:
        """
        Get all available filters for relationships.

        :return: The available filters.
        """
        request = FiltersGetAPI.get_request("relationships")
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return FiltersGetAPI.process_response(response)


class FiltersGetAPIAsyncMixin(BaseAPIAsyncMixin):
    async def get_assets_filters(self) -> List[AvailableSearchFilter]:
        """
        Get all available filters for assets.

        :return: The available filters.
        """
        request = FiltersGetAPI.get_request("asset")
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return FiltersGetAPI.process_response(response)

    async def get_products_filters(self) -> List[AvailableSearchFilter]:
        """
        Get all available filters for products.

        :return: The available filters.
        """
        request = FiltersGetAPI.get_request("product")
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return FiltersGetAPI.process_response(response)

    async def get_relationships_filters(self) -> List[AvailableSearchFilter]:
        """
        Get all available filters for relationships.

        :return: The available filters.
        """
        request = FiltersGetAPI.get_request("relationships")
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return FiltersGetAPI.process_response(response)
