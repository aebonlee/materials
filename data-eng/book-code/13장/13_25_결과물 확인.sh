cd ~/data-eng/week3
ls -lh *.parquet *.csv

python3 -c "
import pandas as pd
d = pd.read_parquet('orders_enriched.parquet')
print('행/열:', d.shape)
print('region 결측:', d['region'].isna().sum())
"
