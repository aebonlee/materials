# 4단계(CTE 따로 보기) — sql_analysis.py 끝에 이어 붙입니다
print(duckdb.sql("""
    SELECT date_trunc('day', ts) AS d, sum(value) AS revenue
    FROM 'events.parquet'
    WHERE event_type = 'buy'
    GROUP BY d
    ORDER BY d
    LIMIT 3
"""))
