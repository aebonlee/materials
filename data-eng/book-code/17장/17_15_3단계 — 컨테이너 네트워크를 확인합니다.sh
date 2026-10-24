# 내 컴퓨터에서 — localhost:9000
curl -s -o /dev/null -w "호스트에서 9000: %{http_code}\n" http://localhost:9000/minio/health/live

# mc 컨테이너 안에서 — 서비스 이름 minio로 붙어 봅니다 (mc 이미지에는 wget·curl이 없어 mc로 확인)
docker compose exec mc mc alias set test http://minio:9000 minioadmin minioadmin
