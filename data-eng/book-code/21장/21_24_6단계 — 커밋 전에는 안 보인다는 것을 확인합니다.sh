# 실패하는 INSERT — 타입이 안 맞습니다
docker compose exec spark-iceberg spark-sql -e \
  "INSERT INTO demo.lakehouse.orders
     VALUES ('없는아이디', 'x', 1, DATE '2026-08-05', 'web', 'm');" 2>&1 | grep -m1 'CANNOT_SAFELY_CAST'
