-- ============================================================
-- THREAD Clothing Store Database
-- schema.sql
-- COP 4710 Final Project -- Group 37
-- Skyler · Rachelle · Jayden · Sabrina
-- ============================================================

CREATE DATABASE IF NOT EXISTS clothing_store;
USE clothing_store;

-- ------------------------------------------------------------
-- TABLE: customers
-- ------------------------------------------------------------
CREATE TABLE customers (
    id         INT           AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50)   NOT NULL,
    last_name  VARCHAR(50)   NOT NULL,
    email      VARCHAR(100)  NOT NULL UNIQUE,
    address    VARCHAR(255),
    member     TINYINT(1)    NOT NULL DEFAULT 0,
    created_at TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_email CHECK (email LIKE '%@%.%')
);

-- ------------------------------------------------------------
-- TABLE: products
-- ------------------------------------------------------------
CREATE TABLE products (
    id             INT            AUTO_INCREMENT PRIMARY KEY,
    name           VARCHAR(100)   NOT NULL,
    category       VARCHAR(50)    NOT NULL DEFAULT 'Uncategorized',
    base_price     DECIMAL(10,2)  NOT NULL,
    stock_quantity INT            NOT NULL DEFAULT 0,
    CONSTRAINT chk_price CHECK (base_price >= 0),
    CONSTRAINT chk_stock CHECK (stock_quantity >= 0)
);

-- ------------------------------------------------------------
-- TABLE: orders
-- ------------------------------------------------------------
CREATE TABLE orders (
    id               INT            AUTO_INCREMENT PRIMARY KEY,
    customer_id      INT            NOT NULL,
    order_date       DATE           NOT NULL DEFAULT (CURRENT_DATE),
    status           VARCHAR(20)    NOT NULL DEFAULT 'pending',
    shipping_address VARCHAR(255),
    total_amount     DECIMAL(10,2)  NOT NULL DEFAULT 0.00,
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id)
        REFERENCES customers(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT chk_status CHECK (status IN ('pending','shipped','delivered','cancelled')),
    CONSTRAINT chk_total  CHECK (total_amount >= 0)
);

-- ------------------------------------------------------------
-- TABLE: order_items
-- ------------------------------------------------------------
CREATE TABLE order_items (
    id         INT            AUTO_INCREMENT PRIMARY KEY,
    order_id   INT            NOT NULL,
    product_id INT            NOT NULL,
    quantity   INT            NOT NULL,
    unit_price DECIMAL(10,2)  NOT NULL,
    CONSTRAINT fk_items_order   FOREIGN KEY (order_id)
        REFERENCES orders(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_items_product FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT chk_qty        CHECK (quantity > 0),
    CONSTRAINT chk_unit_price CHECK (unit_price >= 0)
);

-- ============================================================
-- ADVANCED FEATURE 1: VIEW
-- order_summary joins orders, customers, and order_items into
-- a single readable summary used by the orders page.
-- ============================================================
CREATE OR REPLACE VIEW order_summary AS
SELECT
    o.id                                    AS order_id,
    CONCAT(c.first_name, ' ', c.last_name)  AS customer_name,
    c.email                                 AS customer_email,
    o.order_date,
    o.status,
    o.shipping_address,
    COUNT(oi.id)                            AS item_count,
    SUM(oi.quantity * oi.unit_price)        AS calculated_total
FROM orders o
JOIN customers   c  ON c.id       = o.customer_id
JOIN order_items oi ON oi.order_id = o.id
GROUP BY
    o.id, c.first_name, c.last_name, c.email,
    o.order_date, o.status, o.shipping_address;

-- ============================================================
-- ADVANCED FEATURE 2: TRIGGER
-- After a new order_item is inserted, automatically recalculate
-- and update orders.total_amount to keep it in sync.
-- ============================================================
DELIMITER $$

CREATE TRIGGER trg_update_order_total
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE orders
    SET total_amount = (
        SELECT COALESCE(SUM(quantity * unit_price), 0)
        FROM order_items
        WHERE order_id = NEW.order_id
    )
    WHERE id = NEW.order_id;
END$$

DELIMITER ;
