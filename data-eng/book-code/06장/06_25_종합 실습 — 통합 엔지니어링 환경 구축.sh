# 환경 전체 종료 후 재기동 (볼륨은 유지됩니다)
docker compose down
docker compose up -d

# 표와 데이터가 살아 있는지 확인
docker compose exec db psql -U engineer -d pipeline -c '\dt'
