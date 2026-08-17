SELECT o.id, i.sku
FROM orders o
LEFT JOIN order_items i ON i.order_id = o.id AND i.sku = 'A'
ORDER BY o.id;
