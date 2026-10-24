# 6단계 — transform.py 끝에 이어 붙입니다
print('결측 현황:')
print(df.isna().sum())

# 방법 1 — 결측 행을 버린다
print('버리면:', len(df.dropna(subset=['price'])), '행')

# 방법 2 — 대표값으로 채운다
filled = df['price'].fillna(df['price'].median())
print('중앙값으로 채우면 결측:', filled.isna().sum())

# 방법 3 — 그대로 두고 집계에서 제외 (Pandas 기본 동작)
print('평균(결측 자동 제외):', round(df['price'].mean()))
