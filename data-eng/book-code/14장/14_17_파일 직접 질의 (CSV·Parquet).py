# 6단계(반대 방향) — query.py 끝에 이어 붙입니다. DataFrame을 SQL에서 바로 참조
orders = pd.read_parquet('orders_enriched.parquet')

print(duckdb.sql("""
    SELECT region, count(*) AS cnt, sum(amount) AS total
    FROM orders            -- 파이썬 변수 이름을 그대로 씁니다
    GROUP BY region
    ORDER BY total DESC
"""))
