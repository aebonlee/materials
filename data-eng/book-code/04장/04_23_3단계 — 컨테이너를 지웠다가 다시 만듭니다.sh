# 컨테이너를 완전히 삭제 (볼륨은 건드리지 않습니다)
docker stop pg
docker rm pg
docker ps -a          # pg가 없어야 합니다
docker volume ls      # pgdata는 남아 있어야 합니다

# 같은 볼륨으로 새 컨테이너 생성
docker run -d --name pg \
  -e POSTGRES_PASSWORD=engineer123 \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16

# 다시 뜨는 데 몇 초 걸립니다 — 바로 치면 아직 준비 중이라 실패할 수 있습니다
sleep 3

# 아까 넣은 데이터가 그대로 있는지 확인
docker exec -it pg psql -U postgres -c "SELECT * FROM sensor;"
