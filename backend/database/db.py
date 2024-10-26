import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_USERNAME = os.environ.get("MONGO_USERNAME")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")

"""
Database connection. 
"""


def get_orders_collection():
    client = AsyncIOMotorClient(f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@mongodb/")
    return client.orderdb.orders
