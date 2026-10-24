# 6단계 — sql_analysis.py 끝에 이어 붙입니다
print(duckdb.sql("""
    WITH daily AS (
        SELECT date_trunc('day', ts) AS d, sum(value) AS revenue
        FROM 'events.parquet'
        WHERE event_type = 'buy'
        GROUP BY d
    )
    SELECT d, revenue,
           round(avg(revenue) OVER (
               ORDER BY d ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
           )) AS ma7
    FROM daily
    ORDER BY d
    LIMIT 10
"""))
