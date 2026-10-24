# 같은 자리에서 localhost로 부르면 실패합니다 (자기 자신을 가리키므로)
docker compose exec client curl -s --max-time 3 http://localhost:80 || echo "localhost 로는 실패 — 정상입니다"
