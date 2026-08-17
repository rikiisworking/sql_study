SELECT SUM(amount) AS revenue
FROM orders
WHERE EXISTS (
    SELECT 1
    FROM order_items
    WHERE orders.id = order_items.order_id
);
