from pydantic import BaseModel

"""
Single order schema
"""


class ValueModel(BaseModel):
    px: float
    qty: float
    num: int
    value: float


"""
Stat schema
"""


class StatModel(BaseModel):
    average_value: float
    greater_value: ValueModel
    lesser_value: ValueModel
    total_qty: float
    total_px: float


"""
Bids response schema
"""


class BidsResponseModel(BaseModel):
    bids: StatModel


"""
Asks response schema
"""


class AsksResponseModel(BaseModel):
    asks: StatModel
