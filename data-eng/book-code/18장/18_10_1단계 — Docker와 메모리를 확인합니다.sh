# 순서만 미리 봅니다 — 줄 앞의 # 때문에 붙여 넣어도 실행되지 않습니다
# 1) 환경 구성 1단계 — cd ~/lakehouse → cat > docker-compose.yml << 'EOF' … EOF → mkdir -p scripts → docker compose up -d
# 2) 그 뒤부터 docker compose exec spark-iceberg spark-sql이 됩니다
# 3) 카탈로그 주소는 컨테이너 안에서 http://rest:8181, 내 컴퓨터에서 localhost:8181
