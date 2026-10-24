# Spark에서 같은 값을 냅니다 (새 터미널 — 홈에서 시작하므로 cd부터)
cd ~/lakehouse
docker compose exec spark-iceberg spark-sql -e \
  "SELECT count(*) AS cnt, sum(amount) AS total FROM demo.lakehouse.orders;"
