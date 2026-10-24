# 정리 — 불량 파일은 지우지 않고 격리 폴더로 옮깁니다(랜딩 존은 받은 그대로 보존)
docker compose exec mc mc mv local/raw/orders/orders_bad.csv local/raw/quarantine/orders_bad.csv
