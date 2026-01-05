from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import datetime

class BillItemBase(BaseModel):
    item_name: str
    price: float
    quantity: int
    item_total: float
    discount: float = 0.0

class BillItemCreate(BillItemBase):
    pass

class BillItem(BillItemBase):
    id: int
    bill_id: int

    class Config:
        from_attributes = True

class BillBase(BaseModel):
    customer_name: str
    customer_phone: Union[str, None] = None
    date: datetime
    total_amount: float
    discount: float = 0.0
    status: str = "Unpaid"
    payment_mode: Union[str, None] = None

class BillCreate(BillBase):
    items: List[BillItemCreate]

class Bill(BillBase):
    id: int
    items: List[BillItem]

    class Config:
        from_attributes = True

class BillStatusUpdate(BaseModel):
    status: str
    payment_mode: Optional[str] = None
