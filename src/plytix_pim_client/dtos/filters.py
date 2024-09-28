from dataclasses import dataclass
from enum import StrEnum
from typing import List

from plytix_pim_client.dtos.base import BaseDTO


class OperatorEnum(StrEnum):
    EXISTS = "exists"
    NOT_EXISTS = "!exists"
    EQUALS = "eq"
    NOT_EQUALS = "!eq"
    CONTAINS = "like"
    IN = "in"
    NOT_IN = "!in"
    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUAL = "gte"
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "lte"
    TEXT_SEARCH = "text_search"
    BETWEEN = "bte"


@dataclass(frozen=True, slots=True, kw_only=True)
class SearchFilter(BaseDTO):
    field: str
    operator: OperatorEnum
    value: str | int | float | bool | None | list[str | int | float | bool] = None


@dataclass(frozen=True, slots=True, kw_only=True)
class ProductsRelationshipFilter(BaseDTO):
    id: str
    qty_operator: OperatorEnum
    value: List[str | int | float | bool]


@dataclass(frozen=True, slots=True, kw_only=True)
class RelationshipSearchFilter(BaseDTO):
    relationship_id: str
    operator: OperatorEnum
    product_ids: List[ProductsRelationshipFilter]


@dataclass(frozen=True, slots=True, kw_only=True)
class AvailableSearchFilter(BaseDTO):
    filter_type: str
    key: str
    operators: List[str]
    options: List[str] | None = None
