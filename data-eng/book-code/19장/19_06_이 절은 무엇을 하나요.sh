# ETL 6단계까지 마쳤다면 격리 폴더로 옮겨 둔 파일도 지웁니다(아직이면 오류 줄 — 무시)
docker compose exec mc mc rm local/raw/quarantine/orders_bad.csv
