# 4단계 — sql_analysis.py 끝에 이어 붙입니다
print(duckdb.sql("""
    WITH daily AS (
        SELECT date_trunc('day', ts) AS d, sum(value) AS revenue
        FROM 'events.parquet'
        WHERE event_type = 'buy'
        GROUP BY d
    )
    SELECT d, revenue,
           sum(revenue) OVER (ORDER BY d) AS cum_revenue
    FROM daily
    ORDER BY d
    LIMIT 5
"""))
