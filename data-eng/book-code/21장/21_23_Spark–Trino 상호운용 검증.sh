# 정리 — 임시 카탈로그를 지웁니다
rm catalog/iceberg2.properties
docker compose restart trino
until docker compose exec trino trino --execute "SELECT 1" > /dev/null 2>&1; do sleep 2; done; echo "Trino 준비 완료"
