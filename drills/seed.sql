-- Shared tiny dataset for lessons 0001–0003 drills.
-- Grain notes in comments.

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS cancelled;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

-- grain: one row per customer
CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  region TEXT NOT NULL
);

-- grain: one row per order
CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(id),
  amount REAL NOT NULL,
  status TEXT  -- nullable on purpose (3VL drills)
);

-- grain: one row per line on an order
CREATE TABLE order_items (
  order_id INTEGER NOT NULL REFERENCES orders(id),
  sku TEXT NOT NULL,
  qty INTEGER NOT NULL
);

-- grain: one row per cancel event; order_id may be NULL (3VL trap)
CREATE TABLE cancelled (
  order_id INTEGER
);

INSERT INTO customers (id, region) VALUES
  (10, 'east'),
  (20, 'west');

INSERT INTO orders (id, customer_id, amount, status) VALUES
  (1, 10, 100, 'paid'),
  (2, 10,  50, 'paid'),
  (3, 20, 200, NULL);

INSERT INTO order_items (order_id, sku, qty) VALUES
  (1, 'A', 2),
  (1, 'B', 1),
  (2, 'A', 1),
  (3, 'C', 4);

INSERT INTO cancelled (order_id) VALUES
  (2),
  (NULL);
