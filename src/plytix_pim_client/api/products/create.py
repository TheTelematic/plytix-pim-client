import asyncio
from concurrent.futures.thread import ThreadPoolExecutor
from http import HTTPMethod
from typing import TypedDict

import httpx

from plytix_pim_client.dtos.product import Product
from plytix_pim_client.dtos.request import PlytixRequest
from plytix_pim_client.http.async_ import AsyncClient
from plytix_pim_client.http.sync import SyncClient


class CreateProductDict(TypedDict):
    sku: str
    label: str | None


class ProductCreateAPI:
    @staticmethod
    def get_create_product_request(sku: str, label: str | None = None) -> PlytixRequest:
        data = {"sku": sku}
        if label:
            data["label"] = label

        return PlytixRequest(
            method=HTTPMethod.POST,
            endpoint="/api/v1/products",
            kwargs={"json": data},
        )

    @staticmethod
    def process_create_product_response(response: httpx.Response) -> Product:
        return Product.from_dict(response.json()["data"][0])


class ProductCreateAPISync(ProductCreateAPI):
    def __init__(self, client: SyncClient):
        self.client = client

    def create_product(self, sku: str, label: str | None = None) -> Product:
        """
        Create a product in Plytix PIM.

        :return: The product created.
        """
        request = self.get_create_product_request(sku, label)
        response = self.client.make_request(request.method, request.endpoint, **request.kwargs)
        return self.process_create_product_response(response)

    def create_products(self, products: list[CreateProductDict]) -> list[Product]:
        """
        Create multiple products in Plytix PIM. This uses threading to make the requests concurrently.

        :return: The products created.
        """
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.create_product, **product) for product in products]
            return [future.result() for future in futures]


class ProductCreateAPIAsync(ProductCreateAPI):
    def __init__(self, client: AsyncClient):
        self.client = client

    async def create_product(self, sku: str, label: str | None = None) -> Product:
        """
        Create a product in Plytix PIM.

        :return: The product created.
        """
        request = self.get_create_product_request(sku, label)
        response = await self.client.make_request(request.method, request.endpoint, **request.kwargs)
        return self.process_create_product_response(response)

    async def create_products(self, products: list[CreateProductDict]) -> list[Product]:
        """
        Create multiple products in Plytix PIM. This uses asyncio to make the requests concurrently.

        :param products: The products created.
        """
        return list(await asyncio.gather(*[self.create_product(**product) for product in products]))
