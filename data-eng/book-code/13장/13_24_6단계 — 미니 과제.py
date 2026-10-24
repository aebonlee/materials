# 6단계(미니 과제 정답 예시) — timeseries.py 끝에 이어 붙입니다
cust = m.groupby('customer_id').agg(
    orders=('order_id', 'count'),
    total=('amount', 'sum'),
    last_order=('order_date', 'max'),
).sort_values('total', ascending=False)
print(cust.head(10))

print(m.groupby('weekday')['amount'].mean().round(0).sort_values(ascending=False))

top = (m.groupby(['region', 'category'])['amount'].sum()
         .reset_index()
         .sort_values('amount', ascending=False)
         .groupby('region').head(1))
print(top)
