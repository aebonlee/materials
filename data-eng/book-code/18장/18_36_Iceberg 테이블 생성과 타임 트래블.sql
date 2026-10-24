-- 새로 넣는 행에는 값이 들어갑니다 (spark-sql ()> 에서)
INSERT INTO demo.lakehouse.orders VALUES
  (3, 'park', 19000, DATE '2026-08-02', 'web'),
  (4, 'kim', 27000, DATE '2026-08-02', 'app');

SELECT * FROM demo.lakehouse.orders ORDER BY order_id;
