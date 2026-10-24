ls

# 컨테이너를 지웠다 다시 만들어도 버킷·파일이 남는지 (볼륨 확인 — down -v가 아니라 down)
docker compose down
docker compose up -d
docker compose exec mc mc ls --recursive local/raw
