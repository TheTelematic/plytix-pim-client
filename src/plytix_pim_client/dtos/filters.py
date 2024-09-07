from dataclasses import dataclass
from enum import StrEnum
from typing import List

from plytix_pim_client.dtos.base import BaseDto


class OperatorEnum(StrEnum):
    EXISTS = "exists"
    NOT_EXISTS = "!exists"
    EQUALS = "eq"
    NOT_EQUALS = "!eq"
    CONTAINS = "like"
    MATCHES = "in"
    NOT_MATCHES = "!in"
    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUAL = "gte"
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "lte"
    TEXT_SEARCH = "text_search"
    BETWEEN = "bte"


@dataclass(frozen=True, slots=True, kw_only=True)
class ProductsSearchFilter(BaseDto):
    field: str
    operator: OperatorEnum
    value: str | int | float | bool | None


@dataclass(frozen=True, slots=True, kw_only=True)
class ProductsRelationshipFilter(BaseDto):
    id: str
    qty_operator: OperatorEnum
    value: List[str | int | float | bool]


@dataclass(frozen=True, slots=True, kw_only=True)
class RelationshipSearchFilter(BaseDto):
    relationship_id: str
    operator: OperatorEnum
    product_ids: List[ProductsRelationshipFilter]
