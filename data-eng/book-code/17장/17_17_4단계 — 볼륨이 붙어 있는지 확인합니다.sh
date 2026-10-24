# 볼륨이 붙어 있는지
docker volume ls | grep minio
docker inspect minio --format '{{range .Mounts}}{{.Name}} -> {{.Destination}}{{end}}'

# 컨테이너를 지웠다 다시 만들어도 볼륨이 남는지
docker compose down
docker compose up -d
docker compose ps
docker volume ls | grep minio
