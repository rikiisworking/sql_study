SELECT o.id, i.sku
FROM orders o
LEFT JOIN order_items i ON i.order_id = o.id AND i.sku = 'A'
WHERE o.order_date >= '2024-01-01' AND o.order_date < '2025-01-01'
  AND o.status = 'paid'
  AND NOT EXISTS (
    SELECT 1 FROM cancelled c WHERE c.order_id = o.id
  )
ORDER BY o.id;
