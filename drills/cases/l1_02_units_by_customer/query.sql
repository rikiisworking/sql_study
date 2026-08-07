-- L1 · Total units (qty) per customer.
-- Summing item qty after join to orders is OK (measure lives at item grain).
-- Return columns: customer_id, units
-- Order rows by customer_id ascending.

SELECT o.customer_id, SUM(oi.qty) as units
FROM orders o
JOIN order_items oi 
    ON o.id = oi.order_id
GROUP BY o.customer_id
ORDER BY o.customer_id
