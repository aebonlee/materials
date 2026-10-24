# admin 컨테이너 안에서 db 이름으로 접속되는지 확인
docker compose exec admin sh -c "getent hosts db"
