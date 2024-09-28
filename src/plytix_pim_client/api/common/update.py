from http import HTTPMethod, HTTPStatus
from typing import Generic, TypeVar

import httpx

from plytix_pim_client.dtos.base import BaseDTO
from plytix_pim_client.dtos.request import PlytixRequest

T = TypeVar("T", bound=BaseDTO)


class UpdateResourceAPI(Generic[T]):
    endpoint_prefix: str
    resource_dto_class: T

    @classmethod
    def get_request(cls, resource_id: str, data: dict) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.PATCH,
            endpoint=f"{cls.endpoint_prefix}/{resource_id}",
            kwargs={"json": data},
        )

    @classmethod
    def process_response(cls, response: httpx.Response) -> T | None:
        if response.status_code == HTTPStatus.NOT_FOUND:
            return None
        if data := response.json().get("data", []):
            return cls.resource_dto_class.from_dict(data[0])

        return None
