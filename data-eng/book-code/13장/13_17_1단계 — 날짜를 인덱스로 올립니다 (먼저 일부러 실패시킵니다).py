# timeseries.py — 1~6단계를 이 파일에 이어 붙입니다
import pandas as pd

df = pd.read_parquet('orders_step1.parquet')
customers = pd.read_csv('customers.csv', parse_dates=['joined'])
m = df.merge(customers, on='customer_id', how='left', validate='many_to_one')

# 일부러 실패 — 인덱스가 날짜가 아닌 채로 resample
try:
    m['amount'].resample('D').sum()
except TypeError as e:
    print('예상대로 실패:', e)
