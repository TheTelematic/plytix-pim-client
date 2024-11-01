from datetime import datetime
from http import HTTPStatus, HTTPMethod
from typing import Callable, Optional, TypedDict, NotRequired
from unittest.mock import Mock, call

import httpx
import pytest

from plytix_pim_client import config
from plytix_pim_client.dtos.assets.asset import Asset
from plytix_pim_client.dtos.assets.category import AssetCategory
from plytix_pim_client.dtos.products.attribute import ProductAttribute, ProductAttributeTypeClass
from plytix_pim_client.dtos.products.category import ProductCategory
from plytix_pim_client.dtos.products.product import Product
from plytix_pim_client.dtos.products.relationship import ProductRelationship
from plytix_pim_client.dtos.products.variant import ProductVariant


class ExpectedRequest(TypedDict):
    method: HTTPMethod
    path: str
    json: NotRequired[dict]
    files: NotRequired[dict]


@pytest.fixture(scope="session", autouse=True)
def check_env_vars():
    config.PLYTIX_API_KEY = "foo"
    config.PLYTIX_API_PASSWORD = "bar"
    config.PLYTIX_PIM_BASE_URL = "http://pim.plytix.test"
    config.PLYTIX_AUTH_BASE_URL = "http://auth.plytix.test"
    config.USER_AGENT = f"[Unit Tests] {config.USER_AGENT}"


@pytest.fixture
def api_token() -> str:
    return "test-token"


@pytest.fixture
def response_factory() -> Callable[[HTTPStatus, Optional[dict]], httpx.Response]:
    def factory(status_code: HTTPStatus, json: dict | list[dict] | None = None) -> httpx.Response:
        if json:
            json = {"data": [json]} if isinstance(json, dict) else {"data": json}

        return httpx.Response(request=Mock(), status_code=status_code, json=json)

    return factory


@pytest.fixture
def assert_requests_factory(mock_requests, api_token) -> Callable[[list[ExpectedRequest]], bool]:
    def factory(expected_requests: list[ExpectedRequest]) -> bool:
        assert mock_requests.request.call_args_list == [
            call(
                request["method"],
                request["path"],
                **{k: v for k, v in request.items() if k not in ["method", "path"]},
                headers={
                    "Authorization": f"Bearer {api_token}",
                    "User-Agent": config.USER_AGENT,
                }
            )
            for request in expected_requests
        ]

        return True

    return factory


@pytest.fixture
def new_asset_data_from_url_factory() -> Callable[[], dict]:
    def factory() -> dict:
        return dict(
            url="http://example.test/image.jpg",
            filename=f"test-{str(datetime.now().timestamp()).replace('.', '')}.jpg",
        )

    return factory


# Fixtures
@pytest.fixture
def product(new_product_data) -> Product:
    return Product(**new_product_data)


@pytest.fixture
def product_attribute(new_product_attribute_data) -> ProductAttribute:
    return ProductAttribute(**new_product_attribute_data)


@pytest.fixture
def product_attribute_media(new_product_attribute_data) -> ProductAttribute:
    new_product_attribute_data["type_class"] = ProductAttributeTypeClass.MEDIA
    return ProductAttribute(**new_product_attribute_data)


@pytest.fixture
def product_relationship(new_product_relationship_data) -> ProductRelationship:
    return ProductRelationship(**new_product_relationship_data)


@pytest.fixture
def product_related(product, product_relationship, new_product_data) -> Product:
    new_product_data["sku"] = f"{new_product_data['sku']}-related"
    return Product(
        **new_product_data,
        relationships=[
            {
                "relationship_id": product_relationship.id,
                "label": product_relationship.label,
                "related_products": [{"product_id": product.id, "quantity": 1}],
            }
        ],
    )


@pytest.fixture
def product_variant(product, new_product_data) -> ProductVariant:
    new_product_data["sku"] = f"{new_product_data['sku']}-variant"
    return ProductVariant(**new_product_data, product_type="VARIANT")


@pytest.fixture
def asset_category(new_product_category_data) -> AssetCategory:
    return AssetCategory(**new_product_category_data)


@pytest.fixture
def product_category(new_product_category_data) -> ProductCategory:
    return ProductCategory(**new_product_category_data)


@pytest.fixture
def product_subcategory(new_product_category_data, product_category) -> ProductCategory:
    new_product_category_data["name"] = f"{new_product_category_data['name']}-sub"
    return ProductCategory(parents_ids=[product_category.id], **new_product_category_data)


@pytest.fixture
def asset_subcategory(new_asset_category_data, asset_category) -> AssetCategory:
    new_asset_category_data["name"] = f"{new_asset_category_data['name']}-sub"
    return AssetCategory(parents_ids=[asset_category.id], **new_asset_category_data)


@pytest.fixture
def asset(new_asset_data_from_url_factory) -> Asset:
    return Asset(**new_asset_data_from_url_factory())
