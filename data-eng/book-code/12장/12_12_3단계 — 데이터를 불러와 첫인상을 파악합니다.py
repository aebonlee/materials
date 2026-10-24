# explore.py — 3~6단계를 이 파일에 이어 붙입니다
import pandas as pd

df = pd.read_csv('orders.csv')

print(df.shape)          # (행, 열)
print(df.dtypes)         # 열마다 타입
print(df.head(3))        # 앞 3줄
df.info()                # 결측 수까지 한눈에 (print로 감싸면 끝에 None이 한 줄 더 찍힙니다)
print(df.describe())     # 숫자 열의 기초 통계
