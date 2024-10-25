# book_order_api

The application read books orders from an external [api](https://api.blockchain.com/v3/#getl3orderbook) and save data in a MongoDB. 

There are three endpoints to read data and statistics : 

-/api/book/asks-stats/{symbol}

-/api/book/bids-stats/{symbol}

-/api/book/all-stats/

The First two endpoints return statistics about order book of specific asset, the last endpoint return general statistics about all assets present in the database.

## Run Project

```
docker-compose up -d --build
```

## Insert Order Book

```
docker-compose exec backend python import_orders.py --symbol={symbol}
```

Es :

```
docker-compose exec backend python import_orders.py --symbol="BTC-GBP"
```

## Use application

Visit http://localhost:8000/docs and test endpoints with Swagger UI