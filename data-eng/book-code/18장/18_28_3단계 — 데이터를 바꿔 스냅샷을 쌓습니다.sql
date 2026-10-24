UPDATE demo.lakehouse.orders SET amount = 20000 WHERE order_id = 1;

-- 스냅샷 이력 확인 (committed_at·snapshot_id 열)
SELECT committed_at, snapshot_id, operation
FROM demo.lakehouse.orders.snapshots
ORDER BY committed_at;
