-- Trino에서
SELECT * FROM iceberg.lakehouse.orders ORDER BY order_id;
SELECT count(*) AS cnt, sum(amount) AS total FROM iceberg.lakehouse.orders;
