# 2단계 — sql_analysis.py 끝에 이어 붙입니다
sql_result = duckdb.sql("""
    SELECT c.region,
           count(*)                  AS orders,
           sum(o.price * o.quantity) AS total
    FROM 'orders_step1.parquet' AS o
    JOIN 'customers.csv'        AS c
      ON o.customer_id = c.customer_id
    GROUP BY c.region
    ORDER BY total DESC
""").df()
print(sql_result)
