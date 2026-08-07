-- L2 · Orders that are not cancelled.
-- cancelled has (2) and (NULL). NOT IN over that list never stays TRUE.
-- Prefer NOT EXISTS (or strip nulls). Return order ids ascending.
-- Return column: id
-- Expected: 1 and 3 (2 is cancelled).

SELECT id
FROM orders
WHERE NOT EXISTS (
    SELECT order_id 
    FROM cancelled
    WHERE orders.id = cancelled.order_id
)
ORDER BY id;
