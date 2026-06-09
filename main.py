from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# ── Database setup ────────────────────────────────────────────────────────────

DATABASE_URL = "sqlite+aiosqlite:///./micro_store.db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


# ── Models ────────────────────────────────────────────────────────────────────

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    sku: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    cost: Mapped[float] = mapped_column(Float, nullable=False)
    stock_qty: Mapped[int] = mapped_column(Integer, default=0)
    low_stock_threshold: Mapped[int] = mapped_column(Integer, default=10)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


# ── Dependencies ──────────────────────────────────────────────────────────────

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# ── Lifespan ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


# ── App ───────────────────────────────────────────────────────────────────────

app = FastAPI(title="Micro Store API", lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Micro Store API is running"}