SELECT id
FROM orders
WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01'
  AND status = 'paid'
  AND NOT EXISTS (
    SELECT 1 FROM cancelled c WHERE c.order_id = orders.id
  )
ORDER BY id;
