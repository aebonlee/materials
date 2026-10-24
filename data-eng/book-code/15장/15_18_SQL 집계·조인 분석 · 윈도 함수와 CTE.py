# 5단계 — sql_analysis.py 끝에 이어 붙입니다
print(duckdb.sql("""
    WITH by_customer AS (
        SELECT c.region, o.customer_id,
               sum(o.price * o.quantity) AS total
        FROM 'orders_step1.parquet' AS o
        JOIN 'customers.csv'        AS c
          ON o.customer_id = c.customer_id
        GROUP BY c.region, o.customer_id
    )
    SELECT region, customer_id, total,
           rank() OVER (PARTITION BY region ORDER BY total DESC) AS rnk
    FROM by_customer
    QUALIFY rnk <= 3
    ORDER BY region, rnk
"""))
