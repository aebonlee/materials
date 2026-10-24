cd ~/data-eng/week3
ls -lh

# 있어야 할 것: make_orders.py · orders.csv · orders_raw.parquet · orders_step1.parquet
python3 -c "
import pandas as pd
d = pd.read_parquet('orders_step1.parquet')
print('행/열:', d.shape)
print('열:', d.columns.tolist())
print('날짜 타입:', d['order_date'].dtype)
"
