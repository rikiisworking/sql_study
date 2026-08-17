SELECT customer_id, SUM(amount) AS total
FROM orders
WHERE status = 'paid'
GROUP BY customer_id
HAVING SUM(amount) > 100
ORDER BY customer_id;
