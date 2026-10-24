EXPLAIN
SELECT customer, sum(amount)
FROM iceberg.lakehouse.orders
GROUP BY customer;
