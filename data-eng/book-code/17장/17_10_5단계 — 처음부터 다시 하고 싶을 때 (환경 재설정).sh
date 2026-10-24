cd ~/lakehouse
docker compose down -v
docker ps -a --filter name=minio
docker volume ls --filter name=minio
