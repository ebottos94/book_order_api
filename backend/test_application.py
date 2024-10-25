from fastapi.testclient import TestClient
import pytest
from .main import app
from .import_orders import get_orders
from database.services import insert_book, get_all_orders, get_symbols, get_symbol_book
from mongomock_motor import AsyncMongoMockClient


def get_mock_collection():
    motor_client = AsyncMongoMockClient()
    return motor_client.orderdb.orders


client = TestClient(app=app)


@pytest.mark.asyncio
async def test_db_operations():
    orders_to_insert = get_orders("BTC-GBP")
    collection = get_mock_collection()
    await insert_book(book=orders_to_insert, collection=collection)
    orders = await get_all_orders(collection=collection)
    assert len(orders) == 1
    orders_to_insert = get_orders("BTC-EUR")
    await insert_book(book=orders_to_insert, collection=collection)
    orders = await get_all_orders(collection=collection)
    assert len(orders) == 2
    symbols = await get_symbols(collection=collection)
    assert len(symbols) == len(orders)
    book = await get_symbol_book(symbol="BTC-EUR", collection=collection)
    assert "bids" in book.keys()
    assert "asks" in book.keys()


def test_endpoints():
    response = client.get("/api/book/all-stats/")
    assert response.status_code == 200
    symbols = response.json().keys()
    for s in symbols:
        response = client.get(f"/api/book/asks-stats/{s}")
        assert response.status_code == 200
