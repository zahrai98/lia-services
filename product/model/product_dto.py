from pydantic import BaseModel, Field
from beanie import PydanticObjectId
from typing import List, Optional


class ProductCreateDto(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    price: float 
    description: str


class ProductDeleteDto(BaseModel):
    product_id: PydanticObjectId


class ProductUpdateDto(BaseModel):
    name: Optional[str] = Field(min_length=1, max_length=50)
    price: Optional[float]
    description: Optional[str]


class ProducFindDto(BaseModel):
    product_id: PydanticObjectId


class ProductExistValidationDto(BaseModel):
    product_id: PydanticObjectId
