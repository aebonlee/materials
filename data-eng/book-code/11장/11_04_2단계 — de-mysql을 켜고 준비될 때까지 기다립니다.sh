docker start de-mysql

# 준비됐는지 — 맨 끝 줄이 실행한 날짜의 ready for connections이고 port: 3306이 보이면 준비 완료
docker logs --tail 5 de-mysql
