WITH ranked AS (
  SELECT
    e.customer_id,
    e.status,
    ROW_NUMBER() OVER (
      PARTITION BY e.customer_id
      ORDER BY e.updated_at DESC, e.event_id DESC
    ) AS rn
  FROM events e
)
SELECT r.customer_id, r.status
FROM ranked r
JOIN customers c ON c.id = r.customer_id
WHERE r.rn = 1
  AND c.region = 'east'
ORDER BY r.customer_id;
