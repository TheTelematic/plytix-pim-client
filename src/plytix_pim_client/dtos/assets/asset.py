from dataclasses import dataclass

from plytix_pim_client.dtos.base import BaseDTO


@dataclass(frozen=True, slots=True, kw_only=True)
class Asset(BaseDTO):
    assigned: bool | None = None
    categories: list[str] | None = None
    content_type: str | None = None
    created: str | None = None
    extension: str | None = None
    file_modified: str | None = None
    file_size: int | None = None
    file_type: str | None = None
    filename: str | None = None
    id: str | None = None
    modified: str | None = None
    n_catalogs: int | None = None
    n_products: int | None = None
    public: bool | None = None
    status: str | None = None
    thumbnail: str | None = None
    url: str | None = None
