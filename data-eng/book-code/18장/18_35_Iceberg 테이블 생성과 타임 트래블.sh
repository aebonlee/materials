# ALTER 뒤 — 데이터 파일 수가 그대로인지 (메타데이터만 바뀌었다는 증거)
docker compose exec -T mc mc ls --recursive local/warehouse | grep -c '.parquet'
