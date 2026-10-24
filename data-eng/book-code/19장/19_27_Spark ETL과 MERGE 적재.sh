# 적재 때마다 스냅샷이 쌓인 이력
docker compose exec spark-iceberg spark-sql -e "SELECT committed_at, snapshot_id, operation FROM demo.lakehouse.orders.snapshots ORDER BY committed_at;"
