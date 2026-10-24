# 순서만 미리 봅니다 — 줄 앞의 # 때문에 붙여 넣어도 실행되지 않습니다
# 1) 상호운용 검증 — Trino에서 쓰고 Spark에서 읽기, 반대로도
# 2) 통합 결과물 — cat > scripts/lakehouse_queries.sql << 'EOF' … EOF → docker compose exec -T trino trino < scripts/lakehouse_queries.sql
# 3) 결과물 — docker-compose.yml · catalog · scripts · 다이어그램을 자기 GitHub 저장소에
