# 4단계 — explore.py 끝에 이어 붙입니다
# price는 정수만 넣었는데 float64입니다
print('price dtype :', df['price'].dtype)
print('quantity dtype:', df['quantity'].dtype)

# 이유는 결측(NaN) 때문입니다
print('price 결측 :', df['price'].isna().sum())
print('quantity 결측:', df['quantity'].isna().sum())

# 값 몇 개를 보면 1000이 1000.0으로 보입니다
print(df['price'].head(3).tolist())
