# query.py — 3~6단계를 이 파일에 이어 붙입니다
import duckdb
import pandas as pd

print(duckdb.sql("""
    SELECT event_type, count(*) AS cnt, sum(value) AS total
    FROM 'events.csv'
    GROUP BY event_type
    ORDER BY cnt DESC
"""))
