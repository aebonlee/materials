cd ~/lakehouse
docker compose stop rest
docker compose exec spark-iceberg spark-sql -e "SHOW DATABASES IN demo;" 2>&1 | grep -E "Exception|Caused"
