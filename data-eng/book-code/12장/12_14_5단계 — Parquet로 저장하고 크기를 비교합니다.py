# 5단계 — explore.py 끝에 이어 붙입니다
df.to_parquet('orders_raw.parquet', index=False)

import os
csv_size = os.path.getsize('orders.csv')
pq_size = os.path.getsize('orders_raw.parquet')
print(f'CSV    : {csv_size:,} bytes')
print(f'Parquet: {pq_size:,} bytes  ({pq_size / csv_size:.0%})')
