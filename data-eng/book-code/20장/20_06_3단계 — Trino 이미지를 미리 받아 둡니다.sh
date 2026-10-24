docker pull trinodb/trino:483
docker images --format '{{.Repository}}:{{.Tag}}  {{.Size}}' | grep trino
