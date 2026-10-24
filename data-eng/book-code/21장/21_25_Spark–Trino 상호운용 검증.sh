# Trino에서 행 수 확인 — 안 늘어야 정상
docker compose exec -T trino trino --execute "SELECT count(*) FROM iceberg.lakehouse.orders;"
