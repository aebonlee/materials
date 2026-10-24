# 1) 새로 만든다 (7장 기동 1단계 그대로)
docker run -d --name de-mysql -e MYSQL_ROOT_PASSWORD=dataeng123 -e MYSQL_DATABASE=shop -p 3306:3306 -v de-mysql-data:/var/lib/mysql mysql:9.7

# 2) 처음 만들 때는 port: 0이 먼저 찍히고 10~20초 뒤 port: 3306이 나온다 — 그때까지 기다린다
docker logs --tail 5 de-mysql

# 3) 접속해서 빈 shop 확인 — Empty set이 정상
docker exec -it -e LANG=C.UTF-8 de-mysql mysql -uroot -pdataeng123 shop
