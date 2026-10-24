# INSERT 뒤 (두 번째 터미널)
docker compose exec -T mc mc ls --recursive local/warehouse | grep -c '.parquet'
