docker compose exec spark-iceberg spark-sql --packages org.apache.hadoop:hadoop-aws:3.3.4 -e "SELECT 1;" 2>&1 | grep -E "artifacts copied|^1$"
