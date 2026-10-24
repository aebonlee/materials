# 5단계 — query.py 끝에 이어 붙입니다
# 조건 필터
print(duckdb.sql("""
    SELECT count(*) FROM 'events.csv' WHERE event_type = 'buy'
"""))

# 8장에서 배운 문법이 그대로 통합니다
print(duckdb.sql("""
    WITH daily AS (
        SELECT date_trunc('day', ts) AS d,
               event_type,
               sum(value) AS total
        FROM 'events.csv'
        GROUP BY 1, 2
    )
    SELECT d, event_type, total,
           sum(total) OVER (PARTITION BY event_type ORDER BY d) AS running
    FROM daily
    ORDER BY event_type, d
    LIMIT 6
"""))
