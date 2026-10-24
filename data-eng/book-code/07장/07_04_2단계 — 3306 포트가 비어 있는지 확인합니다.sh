# 지금 3306을 쓰는 컨테이너가 있는지
docker ps --format 'table {{.Names}}\t{{.Ports}}'
