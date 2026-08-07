-- L3 · Customers with at least 2 paid orders; count of those paid orders.
-- Walk: JOIN not required here — FROM orders → WHERE paid → GROUP → HAVING → SELECT → ORDER
-- Return columns: customer_id, paid_orders
-- Order by paid_orders DESC, customer_id ASC.
-- Seed: customer 10 has 2 paid; 20 has 0 paid (status NULL).

SELECT customer_id, COUNT(1) AS paid_orders
FROM orders
WHERE status='paid'
GROUP BY customer_id, status
ORDER BY paid_orders DESC, customer_id ASC