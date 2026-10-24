-- 행 추가
INSERT INTO iceberg.lakehouse.orders
VALUES (99, 'trino_user', 45000, DATE '2026-08-04', 'web');

SELECT count(*) FROM iceberg.lakehouse.orders;

-- 삭제
DELETE FROM iceberg.lakehouse.orders WHERE order_id = 99;
SELECT count(*) FROM iceberg.lakehouse.orders;
