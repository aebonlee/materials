docker start de-mysql

# 준비됐는지 — 맨 끝 줄에 ready for connections와 port: 3306이 함께 보이면 준비 완료(port: 33060 인 X Plugin 줄이 아님)
docker logs --tail 5 de-mysql
