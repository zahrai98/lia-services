from fastapi import Request, Response

from product.model.product_dto import ProductCreateDto, ProductUpdateDto
from product.service import ProductService
from datetime import datetime
from beanie import PydanticObjectId
from app.core.services.error_handler import APIException


class ProductController:

    @classmethod
    async def create_product(cls, data: ProductCreateDto):
        result = await ProductService.create_product(data)
        res = {
            "success": True,
            "result": {
                'product': result
            },
            'message': "product successfully created",
        }
        return res


    @classmethod
    async def get_one_product(cls, product_id: PydanticObjectId):
        result = await ProductService.find_one_product(product_id=product_id)
        res = {
            "success": True,
            "result": {
                'product': result
            },
            'message': "product successfully created",
        }
        return res
    
    
    @classmethod
    async def get_all_products(cls):
        result = await ProductService.find_all_products()
        res = {
            "success": True,
            "result": {
                'product': result
            },
            'message': "product successfully created",
        }
        return res


    @classmethod
    async def delete_product(cls, product_id: PydanticObjectId):
        await ProductService.delete_product(product_id)
        return {
            "success": True,
            'message': "product successfully deleted"
        }


    @classmethod
    async def update_product(cls, product_id: PydanticObjectId, data: ProductUpdateDto):
        product_update_query: dict = data.dict(include={"name", "price", "description"}, exclude_none=True)
        product_update_query.update({'updated_at': datetime.utcnow()})
        product_is_updated = \
            (await ProductService.find_one_and_update_product(product_id, {"$set": product_update_query})) 
        if not product_is_updated:
            raise APIException(
                errors=[
                    {'message': "product is not found", 'errorCode': 610,
                     'type': 'DATABASE_VERIFICATION'}],
                status_code=400,
            )

        updated_product = await ProductService.find_one_product(product_id)

        return {
            "success": True,
            "result": {
                'product': updated_product
            },
            'message': "product successfully updated",
        }
