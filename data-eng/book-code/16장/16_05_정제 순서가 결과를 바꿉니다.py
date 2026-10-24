# 순서 A — 중복 제거 후 중앙값 계산
df = df.drop_duplicates(subset='order_id')
df['price'] = df['price'].fillna(df['price'].median())

# 순서 B — 중복이 있는 채로 중앙값 계산
df['price'] = df['price'].fillna(df['price'].median())
df = df.drop_duplicates(subset='order_id')

# 중복 행이 섞인 채로 재면 두 중앙값이 다를 수 있습니다 (이 데이터에서도 다릅니다 — 실습 4단계).
