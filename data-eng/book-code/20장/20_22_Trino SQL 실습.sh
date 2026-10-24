# Trino가 만든 테이블을 Spark에서 읽어 봅니다 (두 번째 터미널 — trino> 가 아니라 셸에서)
cd ~/lakehouse
docker compose exec spark-iceberg spark-sql -e \
  "SELECT * FROM demo.lakehouse.daily_sales ORDER BY order_date;"
