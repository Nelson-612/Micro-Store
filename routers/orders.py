from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_db
from models import Order, OrderItem, Product, Customer
from schemas import OrderCreate, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse)
async def create_order(data: OrderCreate, db: AsyncSession = Depends(get_db)):
    # Step 1 — check customer exists
    customer = await db.get(Customer, data.customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Step 2 — check all products exist and have enough stock
    for item in data.items:
        product = await db.get(Product, item.product_id)
        if product is None:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if product.stock_qty < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {product.name}. Available: {product.stock_qty}"
            )

    # Step 3 — create the order
    order = Order(customer_id=data.customer_id)
    db.add(order)
    await db.flush()

    # Step 4 — create order items and deduct stock
    for item in data.items:
        product = await db.get(Product, item.product_id)
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price,
        )
        db.add(order_item)
        product.stock_qty -= item.quantity

    # Step 5 — commit everything together
    await db.commit()

    # Step 6 — reload the order with items explicitly
    result = await db.execute(
        select(Order)
        .where(Order.id == order.id)
        .options(selectinload(Order.items))
    )
    return result.scalar_one()


@router.get("", response_model=list[OrderResponse])
async def get_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Order).options(selectinload(Order.items))
    )
    return result.scalars().all()


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Order)
        .where(Order.id == order_id)
        .options(selectinload(Order.items))
    )
    order = result.scalar_one_or_none()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order