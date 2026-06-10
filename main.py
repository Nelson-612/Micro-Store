from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from fastapi import Depends

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


from pydantic import BaseModel
from sqlalchemy import select

# ── Schemas ───────────────────────────────────────────────────────────────────

class ProductCreate(BaseModel):
    name: str
    sku: str
    description: str | None = None
    price: float
    cost: float
    stock_qty: int = 0
    low_stock_threshold: int = 10

class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    description: str | None
    price: float
    cost: float
    stock_qty: int
    low_stock_threshold: int
    is_active: bool

    model_config = {"from_attributes": True}

# ── Routes ────────────────────────────────────────────────────────────────────

@app.post("/products", response_model=ProductResponse)
async def create_product(data: ProductCreate, db: AsyncSession = Depends(get_db)):
    product = Product(**data.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

@app.get("/products", response_model=list[ProductResponse])
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()