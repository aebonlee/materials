-- 첫 스냅샷으로 롤백 (숫자는 첫 snapshot_id로)
CALL demo.system.rollback_to_snapshot('lakehouse.orders', 1234567890123456789);

SELECT * FROM demo.lakehouse.orders ORDER BY order_id;

-- 롤백은 새 스냅샷을 만들지 않습니다 — snapshots는 그대로
SELECT committed_at, snapshot_id, operation
FROM demo.lakehouse.orders.snapshots
ORDER BY committed_at;

-- 대신 history(현재 상태가 어느 스냅샷이었는지의 이력)에 한 줄 늘어납니다
SELECT * FROM demo.lakehouse.orders.history;
