# analyze.py — 2~7단계를 이 파일에 이어 붙입니다
import pandas as pd

df = pd.read_parquet('orders_step1.parquet')
customers = pd.read_csv('customers.csv', parse_dates=['joined'])

# 2단계 — 카테고리별 명명 집계
summary = df.groupby('category').agg(
    orders=('order_id', 'count'),
    total=('amount', 'sum'),
    avg_price=('price', 'mean'),
).round(0).sort_values('total', ascending=False)
print(summary)
print('열 이름:', summary.columns.tolist())
