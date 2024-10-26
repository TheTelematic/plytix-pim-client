from dataclasses import dataclass, field
from enum import StrEnum

from plytix_pim_client.dtos.base import BaseDTO


class ProductAttributeTypeClass(StrEnum):
    TEXT = "TextAttribute"
    MULTILINE = "MultilineAttribute"
    HTML = "HtmlAttribute"
    INT = "IntAttribute"
    DECIMAL = "DecimalAttribute"
    DROPDOWN = "DropdownAttribute"
    MULTISELECT = "MultiSelectAttribute"
    DATE = "DateAttribute"
    URL = "UrlAttribute"
    BOOLEAN = "BooleanAttribute"
    MEDIA = "MediaAttribute"
    MEDIA_GALLERY = "MediaGalleryAttribute"
    COMPLETENESS = "CompletenessAttribute"


@dataclass(frozen=True, slots=True, kw_only=True)
class ProductAttribute(BaseDTO):
    id: str | None = None
    name: str | None = None
    label: str | None = None
    type_class: ProductAttributeTypeClass | None = None
    groups: list = field(default_factory=list)
    options: list[str] = field(default_factory=list)
    attributes: list[dict] = field(default_factory=list)


@dataclass(frozen=True, slots=True, kw_only=True)
class ProductAttributesGroup(BaseDTO):
    id: str | None = None
    name: str | None = None
    attribute_labels: list[str] = field(default_factory=list)
    order: int | None = None
