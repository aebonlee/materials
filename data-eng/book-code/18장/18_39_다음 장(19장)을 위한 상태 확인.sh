cd ~/lakehouse
docker compose ps
docker compose exec spark-iceberg spark-sql -e "SELECT count(*) FROM demo.lakehouse.orders;"
