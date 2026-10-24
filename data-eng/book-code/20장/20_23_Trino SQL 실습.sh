# MinIO에 파일이 생겼는지도
docker compose exec -T mc mc ls --recursive local/warehouse | grep daily_sales | head -n 5
