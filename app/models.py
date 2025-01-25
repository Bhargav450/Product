from pydantic import BaseModel
from typing import Optional
from enum import Enum

# Enum for product categories
class ProductCategory(str, Enum):
    finished = "finished"
    semi_finished = "semi-finished"
    raw = "raw"

# Enum for unit of measure
class UnitOfMeasure(str, Enum):
    mtr = "mtr"
    mm = "mm"
    ltr = "ltr"
    ml = "ml"
    cm = "cm"
    mg = "mg"
    gm = "gm"
    unit = "unit"
    pack = "pack"

# Pydantic model for Product
class ProductBase(BaseModel):
    name: str
    category: ProductCategory
    description: Optional[str] = None
    product_image: Optional[str] = None
    sku: Optional[str] = None
    unit_of_measure: UnitOfMeasure
    lead_time: int

# Pydantic model for the response of product data
class ProductResponse(ProductBase):
    id: int
    created_date: str
    updated_date: str

    class Config:
        orm_mode = True

# Pydantic model for creating a product (without id)
class ProductCreate(ProductBase):
    pass

# Pydantic model for updating a product
class ProductUpdate(ProductBase):
    pass
