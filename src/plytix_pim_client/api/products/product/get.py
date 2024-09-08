import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPMethod, HTTPStatus

import httpx

from plytix_pim_client.api.base import BaseAPISyncMixin, BaseAPIAsyncMixin
from plytix_pim_client.dtos.product import Product
from plytix_pim_client.dtos.request import PlytixRequest


class ProductGetAPI:
    @staticmethod
    def get_get_product_request(product_id: str) -> PlytixRequest:
        return PlytixRequest(            method = (HTTPMethod.GET,)endpoint=f"/api/v1/products/{product_id}",
        )

    @staticmethod
    def process_get_product_response(response: httpx.Response) -> Product | None:
        if response.status_code == HTTPStatus.NOT_FOUND:
            return None

        return Product.from_dict(response.json()["data"][0])


class ProductGetAPISyncMixin(ProductGetAPI, BaseAPISyncMixin):
    def get_product(self, product_id: str) -> Product | None:
        """
        Get a product in Plytix PIM.

        :return: The product.
        """
        request = self.get_get_product_request(product_id)
        response = self.client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return self.process_get_product_response(response)

    def get_products(self, product_ids: list[str]) -> list[Product | None]:
        """
        Get multiple products in Plytix PIM. This uses threading to make the requests concurrently.

        :return: The products.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.get_product, product_id) for product_id in product_ids]
            return [future.result() for future in futures]


class ProductGetAPIAsyncMixin(ProductGetAPI, BaseAPIAsyncMixin):
    async def get_product(self, product_id: str) -> Product | None:
        """
        Get a product in Plytix PIM.

        :return: The product.
        """
        request = self.get_get_product_request(product_id)
        response = await self.client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return self.process_get_product_response(response)

    async def get_products(self, product_ids: list[str]) -> list[Product | None]:
        """
        Get multiple products in Plytix PIM. This uses asyncio to make the requests concurrently.

        :return: The products.
        """
        return list(await asyncio.gather(*[self.get_product(product_id) for product_id in product_ids]))
