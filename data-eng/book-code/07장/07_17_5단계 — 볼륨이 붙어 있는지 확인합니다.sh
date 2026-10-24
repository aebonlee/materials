# 볼륨 목록에 de-mysql-data가 있어야 합니다
docker volume ls | grep de-mysql

# 컨테이너에 실제로 연결됐는지 확인
docker inspect de-mysql --format '{{range .Mounts}}{{.Name}} -> {{.Destination}}{{end}}'
