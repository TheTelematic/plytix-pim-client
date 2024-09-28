import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPStatus
from typing import Tuple

from plytix_pim_client.api.base import BaseAPIAsyncMixin, BaseAPISyncMixin
from plytix_pim_client.api.common.update import UpdateResourceAPI
from plytix_pim_client.dtos.products.product import Product


class ProductUpdateAPI(UpdateResourceAPI):
    endpoint_prefix = "/api/v1/products"
    resource_dto_class = Product


class ProductUpdateAPISyncMixin(BaseAPISyncMixin):
    def update_product(self, product_id: str, data: dict) -> Product | None:
        """
        Update a product.

        :return: The product.
        """
        request = ProductUpdateAPI.get_request(product_id, data)
        response = self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductUpdateAPI.process_response(response)

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


class ProductUpdateAPIAsyncMixin(BaseAPIAsyncMixin):
    async def update_product(self, product_id: str, data: dict) -> Product | None:
        """
        Update a product.

        :return: The product.
        """
        request = ProductUpdateAPI.get_request(product_id, data)
        response = await self._client.make_request(
            request.method, request.endpoint, accepted_error_codes=[HTTPStatus.NOT_FOUND], **request.kwargs
        )
        return ProductUpdateAPI.process_response(response)

    async def update_products(self, product_ids_and_data: list[Tuple[str, dict]]) -> list[Product | None]:
        """
        Update multiple products. This uses asyncio to make the requests concurrently.

        :return: The products.
        """
        return list(
            await asyncio.gather(*[self.update_product(product_id, data) for product_id, data in product_ids_and_data])
        )
