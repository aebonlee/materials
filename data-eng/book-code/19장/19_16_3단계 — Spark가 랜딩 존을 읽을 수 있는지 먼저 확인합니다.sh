docker compose exec spark-iceberg spark-sql -e 'SELECT count(*) FROM csv.`s3a://raw/orders/`;' 2>&1 | grep -m1 'ClassNotFound'
