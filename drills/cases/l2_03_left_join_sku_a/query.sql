-- L2+L3 · List every order once; attach sku only when the line is sku 'A'.
-- Orders with no 'A' line still appear; sku is NULL for them.
-- Wrong pattern: LEFT JOIN ... WHERE i.sku = 'A' (drops non-matches).
-- Return columns: id, sku  ordered by id ascending.
-- Expected: order 1 → A, order 2 → A, order 3 → NULL

SELECT o.id, i.sku
FROM orders o
LEFT JOIN order_items i ON i.order_id = o.id AND i.sku = 'A'
ORDER BY o.id;
