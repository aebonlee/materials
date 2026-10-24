docker compose exec spark-iceberg \
  cat /opt/spark/conf/spark-defaults.conf | grep -i -E "catalog|s3|iceberg"
