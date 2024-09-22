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
    label: str | None = None
    name: str | None = None
    description: str | None = None
    groups: list = field(default_factory=list)
    type_class: ProductAttributeTypeClass | None = None
    created: str | None = None
    modified: str | None = None
    created_at: str | None = None
    created_user_audit: dict | None = field(default_factory=dict)
    modified_user_audit: dict | None = field(default_factory=dict)
    filter_type: str | None = None
