-- ============================================================
-- THREAD Clothing Store Database
-- constraints_test.sql
-- COP 4710 Final Project -- Group 37
--
-- Each statement below is designed to FAIL.
-- Run after schema.sql and data.sql.
-- The expected error is shown in a comment above each test.
-- ============================================================

USE clothing_store;

-- ------------------------------------------------------------
-- TEST 1: NOT NULL violation on first_name
-- Expected error:
--   ERROR 1048 (23000): Column 'first_name' cannot be null
-- ------------------------------------------------------------
INSERT INTO customers (first_name, last_name, email)
VALUES (NULL, 'Doe', 'nulltest@email.com');


-- ------------------------------------------------------------
-- TEST 2: UNIQUE constraint violation on email
-- Expected error:
--   ERROR 1062 (23000): Duplicate entry 'jsmith@email.com'
--   for key 'customers.email'
-- ------------------------------------------------------------
INSERT INTO customers (first_name, last_name, email)
VALUES ('Jane', 'Smith', 'jsmith@email.com');


-- ------------------------------------------------------------
-- TEST 3: CHECK constraint violation -- negative product price
-- Expected error:
--   ERROR 3819 (HY000): Check constraint 'chk_price' is violated.
-- ------------------------------------------------------------
INSERT INTO products (name, category, base_price, stock_quantity)
VALUES ('Bad Shirt', 'Tops', -5.00, 10);


-- ------------------------------------------------------------
-- TEST 4: FOREIGN KEY violation -- order references non-existent customer
-- Expected error:
--   ERROR 1452 (23000): Cannot add or update a child row:
--   a foreign key constraint fails (clothing_store.orders,
--   CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id)
--   REFERENCES customers (id))
-- ------------------------------------------------------------
INSERT INTO orders (customer_id, order_date, status)
VALUES (9999, '2025-04-01', 'pending');


-- ------------------------------------------------------------
-- TEST 5: CHECK constraint violation -- invalid order status value
-- Expected error:
--   ERROR 3819 (HY000): Check constraint 'chk_status' is violated.
-- ------------------------------------------------------------
INSERT INTO orders (customer_id, order_date, status)
VALUES (1, '2025-04-01', 'processing');
