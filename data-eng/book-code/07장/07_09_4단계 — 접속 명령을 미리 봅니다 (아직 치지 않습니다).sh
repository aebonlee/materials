# 순서만 미리 봅니다 — 줄 앞의 # 때문에 붙여 넣어도 실행되지 않습니다
# 1) 기동과 접속 1단계 — 컨테이너 만들기
# docker run -d --name de-mysql -e MYSQL_ROOT_PASSWORD=dataeng123 -e MYSQL_DATABASE=shop -p 3306:3306 -v de-mysql-data:/var/lib/mysql mysql:9.7
# 2) 2단계 — 끝 줄에 port: 3306이 보일 때까지 기다리기
# docker logs --tail 5 de-mysql
# 3) 3단계 — 접속 (-e LANG=C.UTF-8 을 꼭 붙입니다)
# docker exec -it -e LANG=C.UTF-8 de-mysql mysql -uroot -pdataeng123 shop
