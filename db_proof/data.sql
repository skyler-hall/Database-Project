-- ============================================================
-- THREAD Clothing Store Database
-- data.sql
-- COP 4710 Final Project -- Group 37
-- ============================================================

USE clothing_store;

-- ------------------------------------------------------------
-- customers
-- Includes: normal rows, NULL address (allowed), boundary
-- values for first_name and last_name (empty string tests
-- done in constraints_test.sql instead since NOT NULL blocks
-- them), and one member=1 vs member=0.
-- ------------------------------------------------------------
INSERT INTO customers (first_name, last_name, email, address, member) VALUES
('Jane',    'Smith',    'jsmith@email.com',  '123 Oak Ave, Miami, FL',      1),
('Marco',   'Lopez',    'mlopez@email.com',  '456 Coral Way, Orlando, FL',  0),
('Amy',     'Lee',      'alee@email.com',    '789 Palm Dr, Tampa, FL',      1),
('Tyler',   'Chen',     'tchen@email.com',   '321 Bay Blvd, Naples, FL',    0),
('Sam',     'Rivera',   'srivera@email.com', NULL,                          0),
('Jordan',  'Park',     'jpark@email.com',   NULL,                          1);

-- ------------------------------------------------------------
-- products
-- Includes: normal rows, boundary value base_price = 0.00,
-- boundary value stock_quantity = 0 (out of stock).
-- ------------------------------------------------------------
INSERT INTO products (name, category, base_price, stock_quantity) VALUES
('Classic Oxford Shirt',  'Tops',        58.00,  12),
('Slim Chino Pants',      'Bottoms',     72.00,  15),
('Wool Blend Overcoat',   'Outerwear',  195.00,   4),
('Ribbed Knit Sweater',   'Tops',        89.00,   9),
('Canvas Tote Bag',       'Accessories', 34.00,  20),
('High-Waist Denim',      'Bottoms',     95.00,   0),
('Sample Freebie Tee',    'Tops',         0.00,   5);

-- ------------------------------------------------------------
-- orders  (total_amount starts at 0; trigger will recalculate
--          after order_items are inserted)
-- ------------------------------------------------------------
INSERT INTO orders (customer_id, order_date, status, shipping_address) VALUES
(1, '2025-03-01', 'delivered', '123 Oak Ave, Miami, FL'),
(2, '2025-03-03', 'shipped',   '456 Coral Way, Orlando, FL'),
(3, '2025-03-04', 'pending',   '789 Palm Dr, Tampa, FL'),
(4, '2025-03-05', 'pending',   '321 Bay Blvd, Naples, FL'),
(1, '2025-03-06', 'delivered', '123 Oak Ave, Miami, FL'),
(5, '2025-03-07', 'cancelled', NULL);

-- ------------------------------------------------------------
-- order_items  (trigger fires on each insert and updates
--               orders.total_amount automatically)
-- ------------------------------------------------------------
-- Order 1: Jane buys Oxford Shirt + Chino Pants + Canvas Tote
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 58.00),
(1, 2, 1, 72.00),
(1, 5, 1, 34.00);

-- Order 2: Marco buys Wool Blend Overcoat
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(2, 3, 1, 195.00);

-- Order 3: Amy buys 2x Ribbed Knit Sweater
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(3, 4, 2, 89.00);

-- Order 4: Tyler buys High-Waist Denim + Canvas Tote + Oxford Shirt
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(4, 6, 1, 95.00),
(4, 5, 1, 34.00),
(4, 1, 1, 58.00);

-- Order 5: Jane buys Chino Pants + Ribbed Knit Sweater
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(5, 2, 1, 72.00),
(5, 4, 1, 89.00);

-- Order 6: Sam (no address) buys freebie tee (boundary: price=0)
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(6, 7, 1, 0.00);
