# SQL → DataFrame
df = duckdb.sql("SELECT … FROM 'events.parquet'").df()

# DataFrame → SQL (변수 이름을 그대로)
result = duckdb.sql("SELECT … FROM df GROUP BY …").df()

# 다른 형태로도 받을 수 있습니다
duckdb.sql('…').fetchall()   # 튜플의 리스트
duckdb.sql('…').to_arrow_table()   # PyArrow 테이블
