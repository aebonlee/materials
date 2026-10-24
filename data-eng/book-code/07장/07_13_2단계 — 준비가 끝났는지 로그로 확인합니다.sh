# 실시간으로 따라가며 보기 (준비되면 Ctrl+C로 빠져나옵니다)
docker logs -f de-mysql

# 또는 마지막 5줄만 (MySQL 로그는 | tail로는 걸러지지 않습니다 — --tail을 씁니다)
docker logs --tail 5 de-mysql
