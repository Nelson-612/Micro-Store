from pydantic import BaseModel


# ── Product Schemas ───────────────────────────────────────────────────────────

class ProductCreate(BaseModel):
    name: str
    sku: str
    description: str | None = None
    price: float
    cost: float
    stock_qty: int = 0
    low_stock_threshold: int = 10


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    cost: float | None = None
    stock_qty: int | None = None
    low_stock_threshold: int | None = None
    is_active: bool | None = None


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


# ── Customer Schemas ──────────────────────────────────────────────────────────

class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str | None = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None

    model_config = {"from_attributes": True}


from datetime import datetime


# ── Order Schemas ─────────────────────────────────────────────────────────────

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    customer_id: int
    items: list[OrderItemCreate]


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    status: str
    created_at: datetime
    items: list[OrderItemResponse]

    model_config = {"from_attributes": True}