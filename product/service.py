from datetime import datetime

from app.core.services.error_handler import APIException
from product.model.product_dto import ProductDeleteDto, ProductCreateDto, ProductUpdateDto, ProducFindDto
from product.model.product_dao import ProductDao

from beanie import PydanticObjectId
# from aioredis import Redis


class ProductService:

    @classmethod
    async def create_product(cls, data: ProductCreateDto):
        product = await ProductDao.create_product(data)
        return product

    @classmethod
    async def delete_product(cls, product_id: str):
        deleted_product = await ProductDao.delete_product(product_id)
        return deleted_product

    @classmethod
    async def find_one_and_update_product(cls, product_id: str, update_query):
        updated_process = await ProductDao.find_one_and_update_product(product_id, update_query)
        return updated_process

    @classmethod
    async def find_one_product(cls, product_id: str, projection=None):
        return await ProductDao.get_product_by_id(product_id, projection)


    @classmethod
    async def find_all_products(cls, projection=None):
        return await ProductDao.get_products(projection)
