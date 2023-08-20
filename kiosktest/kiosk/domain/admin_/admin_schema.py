from pydantic import BaseModel
from typing import List, Union

class AdminOrderSummary(BaseModel):
    customer_name: str
    menu_name: str
    menu_price: int
    options: List[dict]
    total_price: int
    state: str