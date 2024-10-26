from fastapi.testclient import TestClient
import pytest
from .main import app
from .import_orders import get_orders
from .database.services import insert_book, get_all_orders, get_symbols, get_symbol_book
from .database.db import get_orders_collection
from mongomock_motor import AsyncMongoMockClient


async def get_mock_collection():
    motor_client = AsyncMongoMockClient()
    book = get_orders("BTC-GBP")
    await insert_book(book, motor_client.orderdb.orders)
    book = get_orders("BTC-EUR")
    await insert_book(book, motor_client.orderdb.orders)
    return motor_client.orderdb.orders


app.dependency_overrides[get_orders_collection] = get_mock_collection
client = TestClient(app=app)


@pytest.mark.asyncio
async def test_db_operations():
    collection = await get_mock_collection()
    orders = await get_all_orders(collection=collection)
    assert len(orders) == 2
    symbols = await get_symbols(collection=collection)
    assert len(symbols) == len(orders)
    book = await get_symbol_book(symbol="BTC-EUR", collection=collection)
    assert "bids" in book.keys()
    assert "asks" in book.keys()


def test_endpoints():
    response = client.get("/api/book/all-stats/")
    assert len(response.json().keys()) == 2
    symbols = response.json().keys()
    for s in symbols:
        response = client.get(f"/api/book/asks-stats/{s}")
        assert response.status_code == 200
        response = client.get(f"/api/book/bids-stats/{s}")
        assert response.status_code == 200
