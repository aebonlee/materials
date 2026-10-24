# 볼륨(pgdata)을 데이터 디렉터리에 연결해 실행
docker run -d --name pg \
  -e POSTGRES_PASSWORD=engineer123 \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16

# 뜨는 데 몇 초 걸립니다(처음엔 데이터 폴더를 초기화하느라 3초쯤). 로그로 준비 완료를 확인하세요.
docker logs --tail 5 pg

# 준비됐는지 묻는 한 줄 — accepting connections가 나올 때까지 몇 초 기다렸다 다시 칩니다
docker exec pg pg_isready -U postgres

# 볼륨 생성 확인
docker volume ls

# 컨테이너 안의 psql로 접속해 버전 확인
docker exec -it pg psql -U postgres -c "SELECT version();"
