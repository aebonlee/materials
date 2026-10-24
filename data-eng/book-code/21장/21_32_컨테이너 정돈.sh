# 제2권(Spark)에도 씁니다 — 볼륨은 남기고 정지만
cd ~/lakehouse
docker compose stop

docker compose ps -a
docker volume ls | grep -E "minio|lakehouse"
