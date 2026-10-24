# 각 층을 개수로 세어 보면 구조가 보입니다
docker compose exec -T mc mc ls --recursive local/warehouse | grep -c 'metadata.json'
