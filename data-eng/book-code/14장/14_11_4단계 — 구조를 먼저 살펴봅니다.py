# 4단계 — query.py 끝에 이어 붙입니다
# 어떤 열이 있고 타입이 무엇인지
print(duckdb.sql("DESCRIBE SELECT * FROM 'events.csv'"))

# 앞 몇 줄만
print(duckdb.sql("SELECT * FROM 'events.csv' LIMIT 5"))

# 행 수
print(duckdb.sql("SELECT count(*) FROM 'events.csv'"))
