# 7단계 — sql_analysis.py 끝에 이어 붙입니다
# GROUP BY ALL — 집계가 아닌 열로 알아서 묶어 줍니다
print(duckdb.sql("""
    SELECT event_type, date_trunc('day', ts) AS d, count(*) AS cnt
    FROM 'events.parquet'
    GROUP BY ALL
    ORDER BY d, event_type
    LIMIT 5
"""))

# SELECT * EXCLUDE — 몇 개만 빼고 전부
print(duckdb.sql("SELECT * EXCLUDE (event_id) FROM 'events.parquet' LIMIT 3"))

# 열 이름 패턴으로 집계
print(duckdb.sql("SELECT max(COLUMNS('^value$')) FROM 'events.parquet'"))
