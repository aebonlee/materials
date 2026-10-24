# 5단계(CTE 방식) — sql_analysis.py 끝에 이어 붙입니다. QUALIFY 없이 8장 방식으로도 같은 결과
print(duckdb.sql("""
    WITH by_customer AS (
        SELECT c.region, o.customer_id, sum(o.price * o.quantity) AS total
        FROM 'orders_step1.parquet' AS o
        JOIN 'customers.csv' AS c ON o.customer_id = c.customer_id
        GROUP BY c.region, o.customer_id
    ),
    ranked AS (
        SELECT *, rank() OVER (PARTITION BY region ORDER BY total DESC) AS rnk
        FROM by_customer
    )
    SELECT * FROM ranked WHERE rnk <= 3 ORDER BY region, rnk
"""))
