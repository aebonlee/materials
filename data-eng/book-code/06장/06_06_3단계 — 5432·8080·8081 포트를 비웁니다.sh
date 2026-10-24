# 지금 돌고 있는 컨테이너와 포트
docker ps --format 'table {{.Names}}\t{{.Ports}}'

# 4장에서 쓴 이름들을 멈춥니다 — 없는 이름은 오류만 내고 넘어갑니다
docker stop pg web web2 2>/dev/null
