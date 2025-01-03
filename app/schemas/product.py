from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class PriceHistory(BaseModel):
    price: Decimal
    store: str
    timestamp: datetime

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    brand: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    category: str = Field(..., min_length=1, max_length=100)
    barcode: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    unit: Optional[str] = Field(None, description="e.g., kg, l, piece")
    unit_size: Optional[float] = Field(None, description="Size in the specified unit")

class ProductCreate(ProductBase):
    store: str
    current_price: Decimal

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    brand: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    image_url: Optional[HttpUrl] = None
    current_price: Optional[Decimal] = None

class ProductInDB(ProductBase):
    id: str = Field(..., alias='_id')
    store: str
    current_price: Decimal
    price_history: List[PriceHistory] = []
    created_at: datetime
    updated_at: datetime
    is_available: bool = True

    class Config:
        populate_by_name = True

class ProductResponse(ProductInDB):
    price_history: List[PriceHistory] = []
    average_price: Optional[Decimal] = None
    lowest_price: Optional[Decimal] = None
    highest_price: Optional[Decimal] = None

class ProductComparisonResponse(BaseModel):
    product_id: str
    name: str
    store: str
    current_price: Decimal
    price_difference: Decimal
    percentage_difference: float