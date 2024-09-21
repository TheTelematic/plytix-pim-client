from http import HTTPMethod, HTTPStatus

import httpx

from plytix_pim_client.dtos.request import PlytixRequest


class DeleteResourceAPI:
    endpoint_prefix: str

    @classmethod
    def get_request(cls, resource_id: str) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.DELETE,
            endpoint=f"{cls.endpoint_prefix}/{resource_id}",
        )

    @classmethod
    def process_response(cls, response: httpx.Response) -> bool:
        if response.status_code == HTTPStatus.NOT_FOUND:
            return False
        else:
            return True
