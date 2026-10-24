docker run -d --name de-mysql \
  -e MYSQL_ROOT_PASSWORD=dataeng123 \
  -e MYSQL_DATABASE=shop \
  -p 3306:3306 \
  -v de-mysql-data:/var/lib/mysql \
  mysql:9.7

docker ps
