# 지웠다 다시 만들기
docker stop pg_novol && docker rm pg_novol
docker run -d --name pg_novol -e POSTGRES_PASSWORD=engineer123 -p 5433:5432 postgres:16
sleep 5
docker exec -it pg_novol psql -U postgres -c "SELECT * FROM t;"
