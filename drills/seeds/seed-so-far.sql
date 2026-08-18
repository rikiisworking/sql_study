-- Stacked drill dataset (lessons 0001–0009). Do not edit for practice.
-- Shop tables match seed-integrated.sql; events add version history (0008 / 0009).

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS cancelled;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
  id INTEGER PRIMARY KEY,
  region TEXT NOT NULL
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(id),
  amount REAL NOT NULL,
  status TEXT,
  order_date TEXT NOT NULL
);

CREATE TABLE order_items (
  order_id INTEGER NOT NULL REFERENCES orders(id),
  sku TEXT NOT NULL,
  qty INTEGER NOT NULL
);

CREATE TABLE cancelled (
  order_id INTEGER
);

-- Grain: one row per status-change event (many versions per customer).
CREATE TABLE events (
  event_id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(id),
  updated_at TEXT NOT NULL,
  status TEXT NOT NULL
);

INSERT INTO customers (id, region) VALUES
  (10, 'east'),
  (20, 'west'),
  (30, 'east'),
  (40, 'west'),
  (50, 'east');

INSERT INTO orders (id, customer_id, amount, status, order_date) VALUES
  (1, 10, 100, 'paid', '2024-03-01'),
  (2, 10,  50, 'paid', '2024-06-01'),
  (3, 20, 200, NULL,   '2023-11-01'),
  (4, 20,  80, 'paid', '2024-08-01'),
  (5, 30,  40, 'paid', '2024-02-01'),
  (6, 30,  90, 'paid', '2024-09-01');

INSERT INTO order_items (order_id, sku, qty) VALUES
  (1, 'A', 2),
  (1, 'B', 1),
  (2, 'A', 1),
  (3, 'C', 4),
  (4, 'B', 2),
  (5, 'A', 1),
  (6, 'A', 3),
  (6, 'D', 1);

INSERT INTO cancelled (order_id) VALUES
  (2),
  (NULL);

INSERT INTO events (event_id, customer_id, updated_at, status) VALUES
  (1,  10, '2024-01-01', 'new'),
  (2,  10, '2024-06-01', 'active'),
  (3,  10, '2024-06-01', 'closed'),   -- same-day tie; event_id breaks it
  (4,  20, '2024-03-01', 'new'),
  (5,  30, '2024-02-01', 'new'),
  (6,  30, '2024-04-01', 'active'),
  (7,  30, '2024-07-01', 'paused'),
  (8,  40, '2023-12-01', 'new'),
  (9,  40, '2024-05-01', 'closed'),
  (10, 50, '2024-01-15', 'new'),
  (11, 50, '2025-01-02', 'active');   -- later than 2024; latest-in-2024 trap
