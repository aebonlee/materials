# 순서만 미리 봅니다 — 줄 앞의 # 때문에 붙여 넣어도 실행되지 않습니다
# 1) 구축 1단계 — mkdir -p ~/lakehouse/data → cd ~/lakehouse → cat > docker-compose.yml << 'EOF' … EOF
# 2) docker compose up -d   ← 이 뒤부터 docker compose exec mc … 가 됩니다
# 3) 주소는 컨테이너 안에서 http://minio:9000, 내 컴퓨터(브라우저·boto3)에서 localhost:9000·9001
