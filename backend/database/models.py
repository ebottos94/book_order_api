from pydantic import BaseModel
from typing import List

"""
Order raw schema
"""


class Order(BaseModel):
    px: float
    qty: float
    num: int


"""
Book raw schema for data validation during data ingestion
"""


class Book(BaseModel):
    symbol: str
    bids: List[Order]
    asks: List[Order]
