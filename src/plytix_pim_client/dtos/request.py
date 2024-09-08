from dataclasses import dataclass, field
from http import HTTPMethod

from plytix_pim_client.dtos.base import BaseDto


@dataclass(frozen=True, slots=True, kw_only=True)
class PlytixRequest(BaseDto):
    method: HTTPMethod
    endpoint: str
    kwargs: dict = field(default_factory=dict)
