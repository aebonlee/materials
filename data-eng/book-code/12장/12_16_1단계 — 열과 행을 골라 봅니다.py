# transform.py — 1~8단계를 이 파일에 이어 붙입니다
import pandas as pd
df = pd.read_csv('orders.csv')

# 열 하나 → Series
print(type(df['price']))

# 열 여러 개 → DataFrame (대괄호가 두 겹인 것에 주의)
print(type(df[['order_id', 'price']]))

# 위치로 — iloc (끝 제외)
print(df.iloc[0:3])

# 이름표로 — loc (끝 포함)
print(df.loc[0:2])
