docker pull tabulario/iceberg-rest:1.6.0
docker pull tabulario/spark-iceberg:3.5.5_1.8.1
docker images --format '{{.Repository}}:{{.Tag}}  {{.Size}}' | grep tabulario
