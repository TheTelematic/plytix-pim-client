import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPMethod, HTTPStatus
from typing import Tuple

import httpx

from plytix_pim_client.api.base import BaseAPISyncMixin, BaseAPIAsyncMixin
from plytix_pim_client.dtos.product import Product
from plytix_pim_client.dtos.request import PlytixRequest


class ProductUpdateAPI:
    @staticmethod
    def get_update_product_request(product_id: str, data: dict) -> PlytixRequest:
        return PlytixRequest(
            method=HTTPMethod.PATCH,
            endpoint=f"/api/v1/products/{product_id}",
            kwargs={"json": data},
        )

    @staticmethod
    def process_update_product_response(response: httpx.Response) -> Product | None:
        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        return Product.from_dict(response.json()["data"][0])


class ProductUpdateAPISyncMixin(ProductUpdateAPI, BaseAPISyncMixin):
    def update_product(self, product_id: str, data: dict) -> Product | None:
        """
        Update a product.

        :return: The product.
        """
        request = self.get_update_product_request(product_id, data)
        response = self.client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return self.process_update_product_response(response)

    def update_products(self, product_ids_and_data: list[Tuple[str, dict]]) -> list[Product | None]:
        """
        Update multiple products. This uses threading to make the requests concurrently.

        :return: The products.
        """
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.update_product, product_id, data) for product_id, data in product_ids_and_data
            ]
            return [future.result() for future in futures]


class ProductUpdateAPIAsyncMixin(ProductUpdateAPI, BaseAPIAsyncMixin):
    async def update_product(self, product_id: str, data: dict) -> Product | None:
        """
        Update a product.

        :return: The product.
        """
        request = self.get_update_product_request(product_id, data)
        response = await self.client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return self.process_update_product_response(response)

    async def update_products(self, product_ids_and_data: list[Tuple[str, dict]]) -> list[Product | None]:
        """
        Update multiple products. This uses asyncio to make the requests concurrently.

        :return: The products.
        """
        return list(
            await asyncio.gather(*[self.update_product(product_id, data) for product_id, data in product_ids_and_data])
        )
