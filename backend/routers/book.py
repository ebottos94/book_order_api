from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from ..database.db import get_orders_collection
from ..database.services import get_symbols, get_symbol_book, get_all_orders
from ..database.schema import BidsResponseModel, AsksResponseModel
from ..utils.stats import get_symbol_stats, get_global_stats
from motor.motor_asyncio import AsyncIOMotorCollection

router = APIRouter()

OrderCollection = Annotated[AsyncIOMotorCollection, Depends(get_orders_collection)]

"""
Bids stats endpoint
"""


@router.get("/bids-stats/{symbol}", response_model=BidsResponseModel)
async def bids_stats(symbol: str, order_collection: OrderCollection):
    symbols = await get_symbols(collection=order_collection)
    if symbol not in symbols:
        raise HTTPException(
            status_code=400,
            detail=f"{symbol} is not present in the database. Symbols available are : {symbols}",
        )
    book = await get_symbol_book(symbol=symbol, collection=order_collection)
    stats = get_symbol_stats(book["bids"])
    return {"bids": stats}


"""
Asks stats endpoint
"""


@router.get("/asks-stats/{symbol}", response_model=AsksResponseModel)
async def asks_stats(symbol: str, order_collection: OrderCollection):
    symbols = await get_symbols(collection=order_collection)
    if symbol not in symbols:
        raise HTTPException(
            status_code=400,
            detail=f"{symbol} is not present in the database. Symbols available are : {symbols}",
        )
    book = await get_symbol_book(symbol=symbol, collection=order_collection)
    stats = get_symbol_stats(book["asks"])
    return {"asks": stats}


"""
General stats endpoint
"""


@router.get("/all-stats/")
async def all_stats(order_collection: OrderCollection):
    orders = await get_all_orders(collection=order_collection)
    result = {}
    for o in orders:
        result[o["symbol"]] = {
            "bids": get_global_stats(o["bids"]),
            "asks": get_global_stats(o["asks"]),
        }
    return result
