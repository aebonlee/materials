docker compose exec -T mc mc ls --recursive local/warehouse | grep -c '.parquet'
