import os
from motor.motor_asyncio import AsyncIOMotorClient
from mongomock_motor import AsyncMongoMockClient

MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
IS_TEST = os.environ.get("IS_TEST")

if IS_TEST is None:
    IS_TEST = True
else:
    IS_TEST = False

"""
Database connection. 
If IS_TEST is not present in variable environment we use Mock db to test endpoints
"""


async def get_orders_collection():
    if IS_TEST:
        from ..import_orders import get_orders
        from .services import insert_book

        client = AsyncMongoMockClient()
        book = get_orders("BTC-GBP")
        await insert_book(book, client.orderdb.orders)
    else:
        client = AsyncIOMotorClient(
            f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@mongodb/"
        )
    return client.orderdb.orders
