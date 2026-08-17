SELECT id
FROM orders
WHERE NOT EXISTS (
    SELECT 1
    FROM cancelled
    WHERE orders.id = cancelled.order_id
)
ORDER BY id;
