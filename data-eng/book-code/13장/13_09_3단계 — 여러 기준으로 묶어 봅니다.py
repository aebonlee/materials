# 3단계 — analyze.py 끝에 이어 붙입니다
# 두 열로 묶기 — 결과 인덱스가 두 겹이 됩니다
by2 = df.groupby(['category', 'month']).agg(
    orders=('order_id', 'count'),
    total=('amount', 'sum'),
)
print(by2.head(6))

# 다루기 쉽게 평탄화
flat = by2.reset_index()
print(flat.head(3))
print('행 수:', len(flat))
