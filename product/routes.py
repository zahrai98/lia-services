from beanie import PydanticObjectId
from fastapi import APIRouter, Depends
from product.product_dep import product_exist_validation, delete_product_exist_validation, products_exist_validation
from product.controller import ProductController
from product.model.product_dto import ProductCreateDto, ProductDeleteDto, ProductUpdateDto

router = APIRouter()


@router.post('/')
async def create_product(body: ProductCreateDto):
    return await ProductController.create_product(body)


@router.get('/', dependencies=[Depends(products_exist_validation)])
async def get_all_product():
    return await ProductController.get_all_products()


@router.delete('/{product_id}', dependencies=[Depends(delete_product_exist_validation)])
async def delete_product(product_id: PydanticObjectId):
    return await ProductController.delete_product(ProductDeleteDto(product_id=product_id))


@router.put('/{product_id}', dependencies=[Depends(product_exist_validation)])
async def update_product(product_id: PydanticObjectId, data: ProductUpdateDto):
    return await ProductController.update_product(product_id, data)


@router.get('/{product_id}', dependencies=[Depends(product_exist_validation)])
async def get_product(product_id: PydanticObjectId):
    return await ProductController.get_one_product(product_id)