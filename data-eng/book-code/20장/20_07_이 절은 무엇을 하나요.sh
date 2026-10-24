# 순서만 미리 봅니다 — 줄 앞의 # 때문에 붙여 넣어도 실행되지 않습니다
# 1) 연결 1단계 — mkdir -p catalog → cat > catalog/iceberg.properties << 'EOF' … EOF
# 2) 연결 2단계 — cat > docker-compose.yml << 'EOF' … EOF → docker compose up -d → SERVER STARTED까지 대기
# 3) 그 뒤부터 docker compose exec -it trino trino가 됩니다
