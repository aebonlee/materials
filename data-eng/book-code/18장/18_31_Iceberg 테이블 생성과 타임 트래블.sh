docker compose exec spark-iceberg spark-sql -e "SELECT * FROM demo.lakehouse.orders TIMESTAMP AS OF '2026-10-19 20:00:00' ORDER BY order_id;" 2>/dev/null
