from dataclasses import dataclass
from http import HTTPMethod

from plytix_pim_client.dtos.base import BaseDto


@dataclass(frozen=True, slots=True, kw_only=True)
class PlytixRequest(BaseDto):
    method: HTTPMethod
    endpoint: str
    kwargs: dict
