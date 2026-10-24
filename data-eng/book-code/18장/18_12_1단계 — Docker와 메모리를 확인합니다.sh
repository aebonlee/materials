docker compose down
docker volume rm lakehouse_rest-catalog
docker compose up -d
docker compose exec mc mc ls --recursive local/warehouse
