SELECT o.customer_id, SUM(oi.qty) AS units
FROM orders o
JOIN order_items oi
    ON o.id = oi.order_id
GROUP BY o.customer_id
ORDER BY o.customer_id;
