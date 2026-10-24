# MinIO
curl -s -o /dev/null -w "minio: %{http_code}\n" http://localhost:9000/minio/health/live

# REST 카탈로그 — 설정 JSON을 돌려줍니다
curl -s http://localhost:8181/v1/config | head -c 300; echo

# Spark — 버전 확인
docker compose exec spark-iceberg spark-sql --version 2>&1 | head -n 5
