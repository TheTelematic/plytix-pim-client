from dataclasses import dataclass, field
from http import HTTPMethod

from plytix_pim_client.dtos.base import BaseDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class PlytixRequest(BaseDTO):
    method: HTTPMethod
    endpoint: str
    kwargs: dict = field(default_factory=dict)
