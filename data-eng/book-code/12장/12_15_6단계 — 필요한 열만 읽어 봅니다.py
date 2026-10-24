# 6단계 — explore.py 끝에 이어 붙입니다
# Parquet — 두 열만 읽습니다
slim = pd.read_parquet('orders_raw.parquet', columns=['category', 'price'])
print(slim.shape)
print(slim.columns.tolist())

# CSV — usecols로 지정해도 파일 전체는 읽어야 합니다
slim_csv = pd.read_csv('orders.csv', usecols=['category', 'price'])
print(slim_csv.shape)
