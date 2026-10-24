mkdir -p ~/data-eng/week1/compose-test
cd ~/data-eng/week1/compose-test

cat > docker-compose.yml << 'EOF'
services:
  web:
    image: nginx:1.27
    ports:
      - "8080:80"
EOF

docker compose up -d
docker compose ps
curl http://localhost:8080
docker compose logs web
docker compose down
docker compose ps -a     # 제목 줄만 나오면 정리 끝
