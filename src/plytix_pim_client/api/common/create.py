from http import HTTPMethod
from typing import Generic, TypeVar

import httpx

from plytix_pim_client.dtos.base import BaseDTO
from plytix_pim_client.dtos.request import PlytixRequest

T = TypeVar("T", bound=BaseDTO)


class CreateResourceAPI(Generic[T]):
    endpoint: str
    resource_dto_class: T

    @classmethod
    def get_request(cls, **data) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.POST,
            endpoint=cls.endpoint,
            kwargs={"json": data},
        )

    @classmethod
    def process_response(cls, response: httpx.Response) -> T:
        return cls.resource_dto_class.from_dict(response.json()["data"][0])
