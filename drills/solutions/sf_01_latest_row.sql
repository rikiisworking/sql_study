WITH ranked AS (
  SELECT
    customer_id,
    event_id,
    updated_at,
    status,
    ROW_NUMBER() OVER (
      PARTITION BY customer_id
      ORDER BY updated_at DESC, event_id DESC
    ) AS rn
  FROM events
)
SELECT customer_id, event_id, updated_at, status
FROM ranked
WHERE rn = 1
ORDER BY customer_id;
