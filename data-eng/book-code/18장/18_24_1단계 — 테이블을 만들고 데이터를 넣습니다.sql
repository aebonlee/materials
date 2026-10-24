CREATE DATABASE IF NOT EXISTS demo.lakehouse;

CREATE TABLE demo.lakehouse.orders (
  order_id   BIGINT,
  customer   STRING,
  amount     DOUBLE,
  order_date DATE
) USING iceberg;

INSERT INTO demo.lakehouse.orders VALUES
  (1, 'kim', 15000, DATE '2026-08-01'),
  (2, 'lee', 32000, DATE '2026-08-01');

SELECT * FROM demo.lakehouse.orders ORDER BY order_id;
