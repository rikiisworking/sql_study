SELECT customer_id, COUNT(1) AS paid_orders
FROM orders
WHERE status = 'paid'
GROUP BY customer_id
HAVING COUNT(1) >= 2
ORDER BY paid_orders DESC, customer_id ASC;
