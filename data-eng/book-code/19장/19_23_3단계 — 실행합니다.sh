docker compose exec -T spark-iceberg spark-submit \
  --packages org.apache.hadoop:hadoop-aws:3.3.4 \
  --conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
  --conf spark.hadoop.fs.s3a.access.key=minioadmin \
  --conf spark.hadoop.fs.s3a.secret.key=minioadmin \
  --conf spark.hadoop.fs.s3a.path.style.access=true \
  /home/iceberg/scripts/etl_orders.py 2>&1 | grep -E "원천 행|정제 후 행|total rows"
