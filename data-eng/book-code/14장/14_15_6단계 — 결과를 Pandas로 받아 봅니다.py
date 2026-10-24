# 6단계 — query.py 끝에 이어 붙입니다
df = duckdb.sql("""
    SELECT event_type, count(*) AS cnt, avg(value) AS avg_value
    FROM 'events.csv'
    GROUP BY event_type
    ORDER BY cnt DESC
""").df()          # ← .df()가 DataFrame으로 변환합니다

print(type(df))
print(df)
print(df.dtypes)
