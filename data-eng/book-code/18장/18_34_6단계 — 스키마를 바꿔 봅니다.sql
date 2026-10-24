-- 컬럼 추가는 메타데이터만 바뀝니다
ALTER TABLE demo.lakehouse.orders ADD COLUMN channel STRING;
DESCRIBE demo.lakehouse.orders;

-- 옛 데이터는 NULL로 읽힙니다 (파일을 다시 쓰지 않았으므로)
SELECT order_id, customer, amount, channel FROM demo.lakehouse.orders ORDER BY order_id;
