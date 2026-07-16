# Micro Store API

A RESTful inventory and order management API built with FastAPI, SQLAlchemy, and SQLite.

## Features

- **Product Management** — Create, read, update, and delete products with stock levels, cost, and price
- **Inventory Tracking** — Automatic stock deduction on order creation with low-stock alerts
- **Customer Records** — Manage customers and look up order history
- **Order Management** — Atomic order transactions with rollback on failure
- **JWT Authentication** — Login system with staff and manager roles
- **Role-based Access** — Staff can create orders, managers can edit products

## Tech Stack

- **Python** — FastAPI, SQLAlchemy, Pydantic, Passlib
- **Database** — SQLite with async I/O via aiosqlite
- **Auth** — JWT tokens via python-jose
- **Server** — Uvicorn

## Project Structure

```
Micro Store/
├── main.py           # App entry point and router registration
├── database.py       # Database engine and session setup
├── models.py         # SQLAlchemy ORM models
├── schemas.py        # Pydantic request/response schemas
└── routers/
    ├── auth.py       # Login, register, JWT logic
    ├── products.py   # Product CRUD + low-stock alert
    ├── customers.py  # Customer CRUD
    └── orders.py     # Order creation with stock deduction
```

## Getting Started

### 1. Clone the repo
```
git clone https://github.com/Nelson-612/<repo-name>.git
cd <repo-name>
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Run the server
```
uvicorn main:app --reload
```

### 4. Open Swagger UI
```
http://127.0.0.1:8000/docs
```

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | Register a new user |
| POST | /auth/login | Login and get JWT token |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /products | List all products |
| POST | /products | Create a product |
| GET | /products/{id} | Get a product |
| PATCH | /products/{id} | Update a product |
| DELETE | /products/{id} | Delete a product |
| GET | /products/low-stock | List low stock products |

### Customers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /customers | List all customers |
| POST | /customers | Create a customer |
| GET | /customers/{id} | Get a customer |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /orders | List all orders |
| POST | /orders | Create an order |
| GET | /orders/{id} | Get an order |

## How Orders Work

When an order is created:
1. Validates the customer exists
2. Checks all products have sufficient stock
3. Creates the order and line items atomically
4. Deducts stock from each product
5. Rolls back everything if any step fails

## Environment

No environment variables required for local development. SQLite database is created automatically on first run as `micro_store.db`.
