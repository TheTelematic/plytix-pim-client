# from http import HTTPMethod
#
# import httpx
#
# from plytix_pim_client.dtos.product import Product
# from plytix_pim_client.dtos.request import PlytixRequest
# from plytix_pim_client.http.async_ import AsyncClient
# from plytix_pim_client.http.sync import SyncClient
#
#
# class ProductsSearchAPI:
#     @staticmethod
#     def get_search_products_request(sku: str, label: str | None = None) -> PlytixRequest:
#         return PlytixRequest(
#             method=HTTPMethod.POST,
#             endpoint="/api/v1/products",
#             kwargs={"json": data},
#         )
#
#     @staticmethod
#     def process_create_product_response(response: httpx.Response) -> Product:
#         return Product.from_dict(response.json()["data"][0])
#
#
# class ProductsSearchAPISync(ProductsSearchAPI):
#     def __init__(self, client: SyncClient):
#         self.client = client
#
#     def create_product(self, sku: str, label: str | None = None) -> Product:
#         request = self.get_create_product_request(sku, label)
#         response = self.client.make_request(request.method, request.endpoint, **request.kwargs)
#         return self.process_create_product_response(response)
#
#
# class ProductsSearchAPIAsync(ProductsSearchAPI):
#     def __init__(self, client: AsyncClient):
#         self.client = client
#
#     async def create_product(self, sku: str, label: str | None = None) -> Product:
#         request = self.get_create_product_request(sku, label)
#         response = await self.client.make_request(request.method, request.endpoint, **request.kwargs)
#         return self.process_create_product_response(response)
