docker run -d --name de-mysql -e MYSQL_ROOT_PASSWORD=dataeng123 -e MYSQL_DATABASE=shop -p 3306:3306 -v de-mysql-data:/var/lib/mysql mysql:9.7

# 끝 줄 port: 3306까지 기다린 뒤 접속해 표가 있는지
docker logs --tail 5 de-mysql
docker exec -it -e LANG=C.UTF-8 de-mysql mysql -uroot -pdataeng123 shop
