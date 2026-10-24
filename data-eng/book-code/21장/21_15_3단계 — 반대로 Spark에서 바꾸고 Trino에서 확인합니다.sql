-- [spark-sql]
ALTER TABLE demo.lakehouse.orders ADD COLUMN memo STRING;
UPDATE demo.lakehouse.orders SET memo = 'vip' WHERE order_id = 4;
