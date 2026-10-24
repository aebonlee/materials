# 스크립트가 처음부터 끝까지 도는지 확인 — 파일을 넘기므로 -T
docker compose exec -T trino trino < scripts/lakehouse_queries.sql | head -n 40
