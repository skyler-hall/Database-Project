-- ============================================================
-- THREAD Clothing Store Database
-- queries.sql
-- COP 4710 Final Project -- Group 37
--
-- 8 queries covering: SELECT, JOIN, aggregate, filter,
-- subquery, view, UPDATE, and DELETE.
-- All queries are executed through app.py (Flask backend).
-- ============================================================

USE clothing_store;

-- ------------------------------------------------------------
-- Query 1: Get all products
-- Type: Basic SELECT
-- Used by: GET /products
-- ------------------------------------------------------------
SELECT id, name, category, base_price, stock_quantity
FROM products
ORDER BY category, name;


-- ------------------------------------------------------------
-- Query 2: Get all customers with membership status
-- Type: Basic SELECT with filter
-- Used by: GET /customers
-- ------------------------------------------------------------
SELECT id, first_name, last_name, email, address,
       CASE WHEN member = 1 THEN 'Member' ELSE 'Guest' END AS membership
FROM customers
ORDER BY last_name, first_name;


-- ------------------------------------------------------------
-- Query 3: Get all orders with customer name (JOIN)
-- Type: INNER JOIN across 3 tables
-- Used by: GET /orders
-- ------------------------------------------------------------
SELECT
    o.id            AS order_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    o.order_date,
    o.status,
    o.shipping_address,
    o.total_amount
FROM orders o
JOIN customers c ON c.id = o.customer_id
ORDER BY o.order_date DESC;


-- ------------------------------------------------------------
-- Query 4: Get full order detail with items (JOIN)
-- Type: Multi-table JOIN with parameters
-- Used by: GET /orders/<id>
-- ------------------------------------------------------------
SELECT
    o.id            AS order_id,
    o.order_date,
    o.status,
    o.shipping_address,
    o.total_amount,
    c.first_name,
    c.last_name,
    c.email,
    p.name          AS product_name,
    oi.quantity,
    oi.unit_price,
    (oi.quantity * oi.unit_price) AS line_total
FROM orders o
JOIN customers   c  ON c.id        = o.customer_id
JOIN order_items oi ON oi.order_id = o.id
JOIN products    p  ON p.id        = oi.product_id
WHERE o.id = 1;  -- parameterized in app.py as %s


-- ------------------------------------------------------------
-- Query 5: Revenue and order count per customer (Aggregate)
-- Type: GROUP BY with SUM and COUNT
-- Used by: GET /customers/stats
-- ------------------------------------------------------------
SELECT
    c.id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.email,
    COUNT(DISTINCT o.id)        AS total_orders,
    COALESCE(SUM(o.total_amount), 0) AS total_spent
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.id, c.first_name, c.last_name, c.email
ORDER BY total_spent DESC;


-- ------------------------------------------------------------
-- Query 6: Products low in stock (Subquery / filter)
-- Type: WHERE with subquery threshold
-- Used by: GET /products/low-stock
-- ------------------------------------------------------------
SELECT id, name, category, base_price, stock_quantity
FROM products
WHERE stock_quantity <= (
    SELECT AVG(stock_quantity) / 2
    FROM products
    WHERE stock_quantity > 0
)
ORDER BY stock_quantity ASC;


-- ------------------------------------------------------------
-- Query 7: Query using the order_summary VIEW
-- Type: SELECT from VIEW
-- Used by: GET /orders/summary
-- ------------------------------------------------------------
SELECT
    order_id,
    customer_name,
    customer_email,
    order_date,
    status,
    item_count,
    calculated_total
FROM order_summary
ORDER BY order_date DESC;


-- ------------------------------------------------------------
-- Query 8: Update order status
-- Type: UPDATE with parameterized WHERE
-- Used by: PUT /orders/<id>/status
-- ------------------------------------------------------------
UPDATE orders
SET status = 'shipped'   -- parameterized in app.py as %s
WHERE id = 2;            -- parameterized in app.py as %s
