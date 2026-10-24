# roundtrip.py — 1~4단계를 이 파일에 이어 붙입니다
import duckdb
import pandas as pd

top = duckdb.sql("""
    SELECT user_id, sum(value) AS spend
    FROM 'events.parquet'
    WHERE event_type = 'buy'
    GROUP BY user_id
    ORDER BY spend DESC
    LIMIT 100
""").df()

print(type(top), top.shape)
print('spend 범위:', top['spend'].min(), '~', top['spend'].max())

# 일부러 실패 — 경계를 눈대중으로 정하면?
top['grade'] = pd.cut(top['spend'],
                      bins=[0, 15000, 25000, float('inf')],
                      labels=['B', 'A', 'S'])
print(top['grade'].value_counts())
