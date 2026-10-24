cd ~/data-eng/week1

# 테스트 표 생성
docker compose exec db psql -U engineer -d pipeline -c "CREATE TABLE IF NOT EXISTS week1 (memo TEXT);"
