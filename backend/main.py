from fastapi import FastAPI
from .routers.book import router as BookRouter

app = FastAPI()

app.include_router(BookRouter, tags=["Book"], prefix="/api/book")
