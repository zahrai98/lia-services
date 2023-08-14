from app.core.services.error_handler import APIException
from beanie import PydanticObjectId

from product.service import ProductService

async def product_exist_validation(product_id: PydanticObjectId):
    product = await ProductService.find_one_product(product_id)
    if product is None:
        raise APIException(
            errors=[
                {'message': "product is invalid", 'errorCode': 607,
                 'type': 'DATABASE_VERIFICATION'}],
            status_code=400,
        )
    

async def delete_product_exist_validation(product_id: PydanticObjectId):
    product = await ProductService.find_one_product(product_id)
    if product is None:
        raise APIException(
            errors=[
                {'message': "product is invalid", 'errorCode': 607,
                 'type': 'DATABASE_VERIFICATION'}],
            status_code=400,
        )
    
async def products_exist_validation():
    products = await ProductService.find_all_products()
    if len(products) == 0:
        raise APIException(
            errors=[
                {'message': "there is no product", 'errorCode': 607,
                 'type': 'DATABASE_VERIFICATION'}],
            status_code=400,
        )

