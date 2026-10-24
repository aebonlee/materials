# 컨테이너는 켜 둔 채로 둡니다 (8장에서 그대로 씁니다)
docker ps | grep de-mysql

# 데이터가 남아 있는지
docker exec -it -e LANG=C.UTF-8 de-mysql mysql -uroot -pdataeng123 shop -e "SELECT id, name FROM products ORDER BY id;"

# 컴퓨터를 껐다면 8장을 시작할 때 이 명령으로 다시 켭니다
# docker start de-mysql
