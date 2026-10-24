docker compose exec spark-iceberg spark-sql -e "SHOW TBLPROPERTIES demo.lakehouse.orders ('read.parquet.vectorization.enabled');"
