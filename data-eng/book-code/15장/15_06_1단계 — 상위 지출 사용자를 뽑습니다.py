# sql_analysis.py — 1~7단계를 이 파일에 이어 붙입니다
import duckdb
import pandas as pd

print(duckdb.sql("""
    SELECT user_id, count(*) AS buys, sum(value) AS spend
    FROM 'events.parquet'
    WHERE event_type = 'buy'
    GROUP BY user_id
    ORDER BY spend DESC
    LIMIT 5
"""))
