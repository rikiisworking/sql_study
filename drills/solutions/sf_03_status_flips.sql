WITH lined AS (
  SELECT
    customer_id,
    event_id,
    status,
    LAG(status) OVER (
      PARTITION BY customer_id
      ORDER BY updated_at ASC, event_id ASC
    ) AS prev_status
  FROM events
)
SELECT customer_id, event_id, prev_status, status
FROM lined
WHERE prev_status IS NOT NULL
  AND status <> prev_status
ORDER BY customer_id, event_id;
