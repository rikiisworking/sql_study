SELECT SUM(o.amount) AS revenue
FROM orders o
WHERE o.status = 'paid'
  AND o.order_date >= '2024-01-01'
  AND o.order_date < '2025-01-01'
  AND NOT EXISTS (
    SELECT 1 FROM cancelled c WHERE c.order_id = o.id
  );
