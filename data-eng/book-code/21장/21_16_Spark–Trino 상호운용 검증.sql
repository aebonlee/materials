-- [Trino CLI]
DESCRIBE iceberg.lakehouse.orders;
SELECT order_id, customer, memo FROM iceberg.lakehouse.orders WHERE memo IS NOT NULL;
