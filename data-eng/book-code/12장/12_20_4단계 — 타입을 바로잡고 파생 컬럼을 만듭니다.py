# 4단계 — transform.py 끝에 이어 붙입니다
df['category'] = df['category'].str.strip()
df['order_date'] = pd.to_datetime(df['order_date'])
df = df.assign(amount=df['price'] * df['quantity'])

print(df.dtypes)
print('6월 첫 주 주문:', len(df[df['order_date'] < '2026-06-08']), '건')
print('카테고리:', df['category'].nunique(), '가지')
