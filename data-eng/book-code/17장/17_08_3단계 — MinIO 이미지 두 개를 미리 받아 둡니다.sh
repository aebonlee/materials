docker pull pgsty/minio
docker pull pgsty/mc
docker images --format '{{.Repository}}:{{.Tag}}  {{.Size}}' | grep pgsty
