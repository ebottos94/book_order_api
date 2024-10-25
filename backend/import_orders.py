import argparse
import httpx
import asyncio
from pydantic import ValidationError
from database.db import get_orders_collection
from database.models import Book
from database.services import insert_book


def get_symbols():
    r = httpx.get("https://api.blockchain.com/v3/exchange/symbols")
    return r.json().keys()


def get_orders(symbol: str):
    r = httpx.get(f"https://api.blockchain.com/v3/exchange/l3/{symbol}")
    return r.json()


def validate_orders(orders: dict):
    try:
        Book.model_validate(orders)
    except ValidationError as e:
        raise e


async def main(orders):
    orders_collection = await get_orders_collection()
    await insert_book(book=orders, collection=orders_collection)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--symbol",
        required=True,
        type=str,
        help="symbol of the book to import, es: 'BTC-USD'",
    )
    args = parser.parse_args()
    symbol = args.symbol
    symbols = get_symbols()
    if symbol not in symbols:
        raise ValueError(
            f"{symbol} is not available. Available symbols are : {list(symbols)}"
        )
    orders = get_orders(symbol=symbol)
    validate_orders(orders=orders)
    asyncio.run(main(orders=orders))
