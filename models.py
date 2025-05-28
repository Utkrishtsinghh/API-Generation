from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str

class ProductResponse(BaseModel):
    totalCount: int
    pageNumber: int
    pageSize: int
    products: List[Product]
