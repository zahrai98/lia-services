from beanie import Document
from pydantic import Field, root_validator
from typing import Optional
from datetime import datetime
from product.model.product_dto import ProductCreateDto

from beanie import PydanticObjectId


COLLECTION_NAME = "Products"


class ProductDao:
    class Product(Document):
        id: PydanticObjectId | None = Field(default_factory=PydanticObjectId, alias="_id")
        name: str = Field(min_length=1, max_length=50)
        price: float 
        description: str
        created_at: datetime = datetime.utcnow()
        updated_at: datetime = datetime.utcnow()

        class Settings:
            name = COLLECTION_NAME
            indexes = ["name"]

        class Config:
            schema_extra = {
                "example": {
                    "name": "product1",
                    "price": 13.5,
                    "description": "product 1 descripton",
                }
            }

        @root_validator
        def number_validator(cls, values):
            if values["created_at"]:
                values["created_at"] = datetime.utcnow()
                values["updated_at"] = datetime.utcnow()
            if values["updated_at"]:
                values["updated_at"] = datetime.utcnow()
            return values


    @classmethod
    async def create_product(cls, body: ProductCreateDto):
        product = cls.Product(**body.dict())
        return await cls.Product.insert_one(product)

    @classmethod
    async def get_product_by_id(cls, product_id: PydanticObjectId, projection=None):
        return await cls.Product.find_one({'_id': product_id}).project(projection)

    @classmethod
    async def get_products(cls, projection=None):
        return await cls.Product.find_many().project(projection).to_list()

    @classmethod
    async def find_one_and_update_product(cls, product_id: PydanticObjectId, update_query: dict):
        return await cls.Product.find_one({'_id': product_id}).update(update_query)
    
    @classmethod
    async def delete_product(cls, product_id: PydanticObjectId):
        return await cls.Product.find_one({'_id': product_id}).delete() 