-- L3 · For paid orders only, customers whose SUM(amount) > 100.
-- status filter is row-level → WHERE.
-- SUM threshold is group-level → HAVING.
-- Return columns: customer_id, total  ordered by customer_id.
-- Seed: cust 10 paid 100+50=150; cust 20 has NULL status (not paid) → out.

SELECT customer_id, SUM(amount) AS total
FROM orders
WHERE status = 'paid'
GROUP BY customer_id
    HAVING SUM(amount) > 100

ORDER BY customer_id;
