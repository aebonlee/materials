cd ~/lakehouse
docker compose exec spark-iceberg spark-sql -e "SELECT * FROM demo.lakehouse.orders TIMESTAMP AS OF '2026-09-06 09:00:00';" 2>&1 | grep -m1 'Cannot find'
