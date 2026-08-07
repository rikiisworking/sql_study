-- L1 · Safe order revenue for orders that have at least one item.
-- True total on seed: 100 + 50 + 200 = 350
-- Trap: JOIN order_items then SUM(o.amount) → 450 (order 1 counted twice).
-- Return one column: revenue

SELECT SUM(amount) as revenue 
FROM orders
WHERE EXISTS (
    SELECT 1
    FROM order_items
    WHERE orders.id = order_items.order_id
)