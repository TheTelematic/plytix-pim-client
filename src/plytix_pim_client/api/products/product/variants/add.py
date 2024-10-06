from http import HTTPMethod, HTTPStatus
from typing import Tuple, TypedDict, NotRequired

import httpx

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.dtos.products.variant import ProductVariant
from plytix_pim_client.dtos.request import PlytixRequest


class ProductVariantDict(TypedDict):
    sku: str
    label: NotRequired[str]
    attributes: NotRequired[dict]


class ProductVariantAddAPI:
    @staticmethod
    def get_request(
        product_id: str,
        variant: ProductVariantDict,
    ) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.POST,
            endpoint=f"api/v1/products/{product_id}/variants",
            kwargs={"json": {"variant": variant}},
        )

    @staticmethod
    def process_response(response: httpx.Response) -> ProductVariant | None:
        if response.status_code in [
            HTTPStatus.NOT_FOUND,
        ]:
            return None

        return ProductVariant.from_dict(response.json()["data"][0])


class ProductVariantAddAPISyncMixin(BaseAPISyncMixin):
    def add_variant_to_product(
        self,
        product_id: str,
        sku: str,
        label: str | None = None,
        attributes: dict | None = None,
    ) -> ProductVariant | None:
        """
        Add variant to a product.

        :return: If added successfully.
        """

        variant: ProductVariantDict = {"sku": sku}
        if label:
            variant["label"] = label

        if attributes:
            variant["attributes"] = attributes

        request = ProductVariantAddAPI.get_request(product_id, variant)
        response = self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductVariantAddAPI.process_response(response)

    def add_variant_to_products(
        self, product_ids_and_variants: list[Tuple[str, ProductVariantDict]]
    ) -> list[ProductVariant | None]:
        """
        Add multiple variants to products.
        This NOT uses threading to make the requests concurrently, due to race condition on server side.

        :return: If added successfully each.
        """
        return [self.add_variant_to_product(product_id, **variant) for product_id, variant in product_ids_and_variants]


class ProductVariantAddAPIAsyncMixin(BaseAPIAsyncMixin):
    async def add_variant_to_product(
        self,
        product_id: str,
        sku: str,
        label: str | None = None,
        attributes: dict | None = None,
    ) -> ProductVariant | None:
        """
        Add variant to a product.

        :return: If added successfully.
        """

        variant: ProductVariantDict = {"sku": sku}
        if label:
            variant["label"] = label

        if attributes:
            variant["attributes"] = attributes

        request = ProductVariantAddAPI.get_request(product_id, variant)
        response = await self._client.make_request(
            request.method,
            request.endpoint,
            accepted_error_codes=[
                HTTPStatus.NOT_FOUND,
            ],
            **request.kwargs,
        )
        return ProductVariantAddAPI.process_response(response)

    async def add_variant_to_products(
        self, product_ids_and_variants: list[Tuple[str, ProductVariantDict]]
    ) -> list[ProductVariant | None]:
        """
        Add multiple variants to products.
        This NOT uses asyncio to make the requests concurrently, due to race condition on server side.

        :return: If added successfully each.
        """
        return [
            await self.add_variant_to_product(product_id, **variant) for product_id, variant in product_ids_and_variants
        ]
