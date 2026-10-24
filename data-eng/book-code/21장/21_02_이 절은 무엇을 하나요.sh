docker compose ps
docker compose exec -T trino trino --execute "SHOW TABLES FROM iceberg.lakehouse;"
