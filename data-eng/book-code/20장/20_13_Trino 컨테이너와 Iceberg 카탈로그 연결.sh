docker compose up -d
until docker compose logs trino | grep -q "SERVER STARTED"; do sleep 2; done; echo "Trino 준비 완료"
docker compose ps
