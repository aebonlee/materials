docker compose exec -T trino trino --execute "SELECT count(*) FROM iceberg.lakehouse.orders;"
