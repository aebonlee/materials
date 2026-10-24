cd ~/lakehouse
ls
ls catalog scripts

# 환경을 내렸다 올려도 같은 상태가 되는지
docker compose down
docker compose up -d
until docker compose exec trino trino --execute "SELECT 1" > /dev/null 2>&1; do sleep 2; done; echo "Trino 준비 완료"
