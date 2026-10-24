cd ~/lakehouse
docker compose up -d
until docker compose exec trino trino --execute "SELECT 1" > /dev/null 2>&1; do sleep 2; done; echo "Trino 준비 완료"
