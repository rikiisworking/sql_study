SELECT o.id AS order_id, i.sku, o.amount * i.qty AS line_total
FROM orders o
JOIN order_items i ON i.order_id = o.id
WHERE o.amount * i.qty > 100
ORDER BY order_id, sku;
