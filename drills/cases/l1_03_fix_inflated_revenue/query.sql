-- L1 · This query is WRONG (fan-out). Fix it.
-- Goal: total order.amount for all orders that appear in order_items.
-- Expected revenue: 350
-- Return one column: revenue

SELECT SUM(o.amount) AS revenue
FROM orders o
WHERE EXISTS (
    SELECT 1
    FROM order_items
    WHERE order_items.order_id = o.id
)

