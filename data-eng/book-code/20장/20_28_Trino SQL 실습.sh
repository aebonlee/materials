docker compose exec spark-iceberg spark-sql -e "ALTER TABLE demo.lakehouse.orders SET TBLPROPERTIES ('read.parquet.vectorization.enabled'='false');"
