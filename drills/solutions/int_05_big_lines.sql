SELECT o.id AS order_id, i.sku, o.amount * i.qty AS line_total
FROM orders o
JOIN order_items i ON i.order_id = o.id
WHERE o.order_date >= '2024-01-01' AND o.order_date < '2025-01-01'
  AND o.status = 'paid'
  AND NOT EXISTS (
    SELECT 1 FROM cancelled c WHERE c.order_id = o.id
  )
  AND o.amount * i.qty > 100
ORDER BY order_id, sku;
