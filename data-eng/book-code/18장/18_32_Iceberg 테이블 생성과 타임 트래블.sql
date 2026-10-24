-- 두 시점을 한 쿼리로 비교할 수도 있습니다 (숫자는 첫 snapshot_id로)
SELECT '이전' AS ver, order_id, amount
FROM demo.lakehouse.orders VERSION AS OF 1234567890123456789
UNION ALL
SELECT '현재', order_id, amount
FROM demo.lakehouse.orders
ORDER BY order_id, ver;
