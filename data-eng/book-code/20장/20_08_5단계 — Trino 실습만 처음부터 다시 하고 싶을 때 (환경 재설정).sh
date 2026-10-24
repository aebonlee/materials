cd ~/lakehouse
docker compose exec spark-iceberg spark-sql -e "DROP TABLE IF EXISTS demo.lakehouse.daily_sales PURGE;"
