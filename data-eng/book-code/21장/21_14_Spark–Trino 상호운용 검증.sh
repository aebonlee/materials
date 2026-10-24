# [Spark] 같은 테이블을 Spark에서 조회
docker compose exec spark-iceberg spark-sql -e \
  "SELECT * FROM demo.lakehouse.orders ORDER BY order_id;"
