from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorCollection

"""
Get a specific book
"""


async def get_symbol_book(symbol: str, collection: AsyncIOMotorCollection):
    book = await collection.find_one({"symbol": symbol}, {"_id": 0})
    return book


"""
Get all symbols in the db
"""


async def get_symbols(collection: AsyncIOMotorCollection):
    documents = await collection.find({}, {"symbol": 1}).to_list(None)
    symbols = [doc["symbol"] for doc in documents]
    return symbols


"""
Get all orders in the db
"""


async def get_all_orders(collection: AsyncIOMotorCollection):
    result = await collection.find({}, {"_id": 0}).to_list(None)
    return result


async def insert_book(book: dict, collection: AsyncIOMotorCollection):
    result = await collection.update_one(
        {"symbol": book["symbol"]},
        {
            "$set": {
                "bids": book["bids"],
                "asks": book["asks"],
                "date": datetime.now(tz=timezone.utc),
            }
        },
        upsert=True,
    )

    if result.upserted_id is not None:
        print(f"{book['symbol']} Book inserted correctly")
    else:
        print(f"{book['symbol']} Book updated correctly")
