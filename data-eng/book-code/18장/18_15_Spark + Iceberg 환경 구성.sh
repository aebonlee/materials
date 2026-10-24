mkdir -p scripts
docker compose up -d
docker compose ps
docker compose exec mc mc mb -p local/warehouse
