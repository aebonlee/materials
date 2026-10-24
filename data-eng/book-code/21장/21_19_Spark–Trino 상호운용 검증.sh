docker compose exec -T trino trino --execute \
  'SELECT count(*) AS snapshot_count FROM iceberg.lakehouse."orders$snapshots";'
