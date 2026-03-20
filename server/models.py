from pydantic import BaseModel
from typing import List
from datetime import datetime

PRINTING_PRICES = {
    "black_and_white": 2.00,
    "colored": 5.00,
    "photo_paper": 20.00
}

class PrintingItem(BaseModel):
    printing_type: str 
    pages: int
    document_name: str

class CreateOrderRequest(BaseModel):
    customer_name: str
    items: List[PrintingItem]
    payment_amount: float

class Order(BaseModel):
    order_id: int
    customer_name: str
    items: List[PrintingItem]
    total_cost: float
    payment_amount: float
    change: float
    created_at: datetime

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    success: bool
    message: str
    data: Order = None