-- L3 · Keep only lines where amount * qty > 100.
-- Toy metric: line_total = orders.amount * order_items.qty (alias practice, not real revenue).
-- Starter returns every line — too many rows.
-- Portable SQL: SELECT aliases are not available in WHERE (WHERE runs first).
--   SQLite may still accept the alias; prefer repeat expression or subquery/CTE.
-- Return columns: order_id, sku, line_total
-- Order by order_id, sku.

SELECT o.id AS order_id, i.sku, o.amount * i.qty AS line_total
FROM orders o
JOIN order_items i ON i.order_id = o.id
WHERE o.amount * i.qty > 100
ORDER BY order_id, sku;
