# 방법 A — 여러 함수를 리스트로 (열 이름이 두 겹이 됩니다)
df.groupby('category').agg({'amount': ['sum', 'mean']})
#   결과 열: ('amount','sum'), ('amount','mean')  ← 다루기 번거롭다

# 방법 B — 명명 집계 (권장)
df.groupby('category').agg(
    orders=('order_id', 'count'),
    total=('amount', 'sum'),
    avg_price=('price', 'mean'),
)
#   결과 열: orders, total, avg_price  ← 한 겹, 이름도 내가 정한 대로
