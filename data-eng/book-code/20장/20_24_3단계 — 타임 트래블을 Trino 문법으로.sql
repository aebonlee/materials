SELECT committed_at, snapshot_id, operation
FROM iceberg.lakehouse."orders$snapshots"
ORDER BY committed_at;

-- 과거 스냅샷 시점 조회 — 아래 숫자를 위 결과 첫 줄의 snapshot_id로 바꿉니다
SELECT * FROM iceberg.lakehouse.orders
FOR VERSION AS OF 1234567890123456789;
