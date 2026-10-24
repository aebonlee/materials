cd ~/lakehouse
docker compose exec spark-iceberg spark-sql -e "SELECT * FROM demo.lakehouse.orders ORDER BY order_id;" 2>&1 | grep -m1 'Cannot support'
