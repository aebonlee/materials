# 2단계 — transform.py 끝에 이어 붙입니다
# 조건 필터 — 불리언 인덱싱
food = df[df['category'].str.strip() == '식품']
big = df[(df['price'] >= 100000) & (df['quantity'] >= 3)]
print('식품 주문:', len(food), '건 / 고액·다수량:', len(big), '건')

# loc — 행 조건과 열 목록을 한 번에
sub = df.loc[df['customer_id'].isin([1, 2, 3]),
             ['order_id', 'customer_id', 'price']]
print(sub.head(3))
