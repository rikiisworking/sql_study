SELECT o.customer_id, SUM(o.amount) AS total
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE c.region = 'east'
  AND o.order_date >= '2024-01-01' AND o.order_date < '2025-01-01'
  AND o.status = 'paid'
  AND NOT EXISTS (
    SELECT 1 FROM cancelled x WHERE x.order_id = o.id
  )
GROUP BY o.customer_id
HAVING SUM(o.amount) >= 100
ORDER BY o.customer_id;
