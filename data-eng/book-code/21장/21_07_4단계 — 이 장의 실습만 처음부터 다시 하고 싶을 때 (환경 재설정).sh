cd ~/lakehouse
docker compose exec -T trino trino --execute "DELETE FROM iceberg.lakehouse.orders WHERE order_id = 8"
