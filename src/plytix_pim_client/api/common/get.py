from http import HTTPMethod, HTTPStatus

import httpx

from plytix_pim_client.dtos.base import BaseDTO
from plytix_pim_client.dtos.request import PlytixRequest


class GetResourceAPI:
    endpoint_prefix: str
    resource_dto_class: BaseDTO

    @classmethod
    def get_request(cls, resource_id: str) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.GET,
            endpoint=f"{cls.endpoint_prefix}/{resource_id}",
        )

    @classmethod
    def process_response(cls, response: httpx.Response) -> BaseDTO | None:
        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        return cls.resource_dto_class.from_dict(response.json()["data"][0])
