# 행 수만으로는 부족합니다 — 키 중복과 합계까지 봅니다
docker compose exec spark-iceberg spark-sql -e "SELECT count(*) AS n_rows, count(DISTINCT order_id) AS n_keys, sum(amount) AS total FROM demo.lakehouse.orders;"
