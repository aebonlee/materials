sudo systemctl enable --now docker
docker version --format '{{.Server.Version}}'
docker pull pgsty/minio
docker pull pgsty/mc
