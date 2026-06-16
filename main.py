from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, Base
from routers import products, customers, orders
import models


@asynccontextmanager
async def lifespan(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Micro Store API", lifespan=lifespan)

app.include_router(products.router)
app.include_router(customers.router)
app.include_router(orders.router)


@app.get("/")
async def root():
    return {"message": "Micro Store API is running"}