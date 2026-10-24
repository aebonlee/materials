# 볼륨 없이 띄우기 (포트는 5433으로 — 5432는 pg가 쓰고 있습니다)
docker run -d --name pg_novol \
  -e POSTGRES_PASSWORD=engineer123 \
  -p 5433:5432 \
  postgres:16

sleep 5
docker exec -it pg_novol psql -U postgres -c "CREATE TABLE t (id int); INSERT INTO t VALUES (1);"
