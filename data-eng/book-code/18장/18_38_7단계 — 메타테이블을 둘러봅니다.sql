-- 스냅샷 이력
SELECT * FROM demo.lakehouse.orders.snapshots;

-- 커밋 이력 (부모 스냅샷 관계까지)
SELECT * FROM demo.lakehouse.orders.history;

-- 현재 유효한 데이터 파일 목록과 통계
SELECT file_path, record_count, file_size_in_bytes
FROM demo.lakehouse.orders.files;

-- 매니페스트 목록
SELECT * FROM demo.lakehouse.orders.manifests;
