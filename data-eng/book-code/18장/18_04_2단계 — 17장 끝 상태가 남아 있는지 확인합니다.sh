cd ~/lakehouse
docker compose up -d
docker compose ps
docker compose exec mc mc ls --recursive local/raw
