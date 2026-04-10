# THREAD — Clothing Store Database Application

## Overview

THREAD is a relational database application for managing a clothing store.
It uses a MySQL database, a Python Flask backend, and an HTML/CSS/JavaScript frontend.

**COP 4710 — Database Final Project | Group 37**
Skyler · Rachelle · Jayden · Sabrina

---

## Technologies

- Python 3 (Flask, mysql-connector-python, flask-cors)
- MySQL 8.0+
- HTML / CSS / JavaScript (vanilla)

---

## Project Structure

```
final_project/
│
├── report.pdf
├── README.md
│
├── backend/
│   └── app.py
│
├── frontend/
│   ├── index.html
│   ├── products.html
│   ├── customers.html
│   ├── orders.html
│   ├── style.css
│   └── app.js
│
└── db_proof/
    ├── schema.sql
    ├── data.sql
    ├── constraints_test.sql
    ├── queries.sql
    └── query_outputs.txt
```

---

## Setup Instructions

### 1. Create the database

Open MySQL and run the two SQL files in order:

```sql
source db_proof/schema.sql
source db_proof/data.sql
```

This creates the `clothing_store` database with all 4 tables, the
`order_summary` view, the `trg_update_order_total` trigger, and
inserts sample data.

### 2. Install Python dependencies

```bash
pip install flask mysql-connector-python flask-cors
```

### 3. Configure database credentials

Open `backend/app.py` and update the connection block if needed:

```python
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",        # set your MySQL password here
    database="clothing_store"
)
```

### 4. Run the backend server

```bash
cd backend
python app.py
```

The API will be available at: **http://127.0.0.1:5000/**

### 5. Open the frontend

Open `frontend/index.html` in a browser. The frontend will
automatically connect to the running Flask server.

---

## API Endpoints

| Method | Endpoint                  | Description                          |
|--------|---------------------------|--------------------------------------|
| GET    | /products                 | All products (Query 1)               |
| GET    | /products/low-stock       | Products below avg stock (Query 6)   |
| GET    | /products/\<id\>          | Single product by ID                 |
| POST   | /products                 | Add a new product                    |
| PUT    | /products/\<id\>          | Update a product                     |
| DELETE | /products/\<id\>          | Delete a product                     |
| GET    | /customers                | All customers with membership (Q2)   |
| GET    | /customers/stats          | Revenue per customer (Query 5)       |
| POST   | /customers                | Add a new customer                   |
| GET    | /orders                   | All orders with customer name (Q3)   |
| GET    | /orders/summary           | Order summary via VIEW (Query 7)     |
| GET    | /orders/\<id\>            | Full order detail with items (Q4)    |
| PUT    | /orders/\<id\>/status     | Update order status (Query 8)        |
| POST   | /orders                   | Create order (transaction-wrapped)   |

---

## Advanced Database Features

**View — `order_summary`**
Joins orders, customers, and order_items into a denormalized summary
used by GET /orders/summary. Defined in schema.sql.

**Trigger — `trg_update_order_total`**
Fires AFTER INSERT on order_items. Automatically recalculates and
updates orders.total_amount so it always reflects the real line-item
sum without manual calculation in the application layer.

**Transaction — POST /orders**
The order creation endpoint wraps the orders INSERT and all
order_items INSERTs in a single transaction. If any insert fails,
the entire order is rolled back.

---

## Constraint Tests

Run `db_proof/constraints_test.sql` after loading the schema and data
to verify that all constraints are enforced. Each statement is designed
to fail with a specific error (NOT NULL, UNIQUE, CHECK, FOREIGN KEY).
