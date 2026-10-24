cat > docker-compose.yml << 'EOF'
services:
  web:
    image: nginx:1.27
    ports:
      - "8080:80"

  client:
    image: curlimages/curl:8.10.1
    command: sleep infinity   # 계속 떠 있게 해서 실험에 씁니다
    depends_on:
      - web
EOF

docker compose up -d

# client 안에서 web을 서비스 이름으로 불러 봅니다
docker compose exec client curl -s http://web:80 | head -n 5
