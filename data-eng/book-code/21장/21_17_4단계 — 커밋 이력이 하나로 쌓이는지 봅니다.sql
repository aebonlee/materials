-- [Trino CLI] 이 부 전체 커밋 이력
SELECT committed_at, snapshot_id, operation
FROM iceberg.lakehouse."orders$snapshots"
ORDER BY committed_at;
