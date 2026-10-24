# db 서비스의 psql로 직접 확인
docker compose exec db psql -U engineer -d pipeline -c "SELECT current_database();"
