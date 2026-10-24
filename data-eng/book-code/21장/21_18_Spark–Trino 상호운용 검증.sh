# Spark 에서도 같은 이력이 보이는지
docker compose exec spark-iceberg spark-sql -e \
  "SELECT count(*) AS snapshot_count FROM demo.lakehouse.orders.snapshots;"
