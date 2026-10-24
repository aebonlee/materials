# 카탈로그가 어디에 저장되는지 · 로그 끝에 Started가 있는지
docker compose logs rest | grep -o "uri=[^,}]*"
docker compose logs rest | tail -n 3
