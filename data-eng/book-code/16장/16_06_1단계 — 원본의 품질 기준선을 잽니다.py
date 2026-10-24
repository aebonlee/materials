# baseline.py — 1단계 두 블록을 이 파일에 이어 붙입니다
import duckdb

baseline = duckdb.sql("""
    SELECT count(*)                                AS rows,
           count(*) - count(price)                 AS null_price,
           count(*) - count(DISTINCT order_id)     AS dup_orders,
           count(DISTINCT category)                AS category_values
    FROM 'orders.csv'
""").df()
print(baseline)
