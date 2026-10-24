# 컨테이너를 지웠다 다시 만들어도 테이블이 남는지 (카탈로그 볼륨 확인 — down -v가 아니라 down)
docker compose down
docker compose up -d
docker compose exec spark-iceberg spark-sql -e "SELECT count(*) FROM demo.lakehouse.orders;"
