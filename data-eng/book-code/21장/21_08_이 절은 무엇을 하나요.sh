docker compose exec spark-iceberg spark-sql -e "ALTER TABLE demo.lakehouse.orders DROP COLUMN memo;"
