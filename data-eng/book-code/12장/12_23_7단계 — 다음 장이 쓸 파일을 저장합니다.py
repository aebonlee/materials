# 7단계 — transform.py 끝에 이어 붙입니다
df.to_parquet('orders_step1.parquet', index=False)

check = pd.read_parquet('orders_step1.parquet')
print('CSV로 읽은 날짜 타입   :', pd.read_csv('orders.csv')['order_date'].dtype)
print('Parquet로 읽은 날짜 타입:', check['order_date'].dtype)
print('저장된 열:', check.columns.tolist())
