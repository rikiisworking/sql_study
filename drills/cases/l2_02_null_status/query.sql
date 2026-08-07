-- L2 · Orders whose status is missing.
-- Never use status = NULL. Return id ascending.
-- Return column: id

SELECT id
FROM orders
WHERE status is NULL
ORDER BY id;
