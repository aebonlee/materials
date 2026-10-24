cd ~/data-eng/week1

# 완전히 내리기 (이번에는 볼륨까지 — 처음부터 올라오는지 보기 위해)
docker compose down -v

# README에 적은 그대로 실행
docker compose up -d --build
docker compose ps -a

# 앱 로그와 DB 접속 확인
docker compose logs app
docker compose exec db psql -U engineer -d pipeline -c "SELECT current_database();"
