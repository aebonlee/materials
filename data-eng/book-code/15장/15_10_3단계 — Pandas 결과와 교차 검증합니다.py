# 3단계 — sql_analysis.py 끝에 이어 붙입니다 (sql_result는 2단계에서 만들었습니다)
pd_result = (pd.read_parquet('orders_enriched.parquet')
             .groupby('region')
             .agg(orders=('order_id', 'count'),
                  total=('amount', 'sum'))
             .reset_index()
             .sort_values('total', ascending=False))
print(pd_result)

# 지역별 total을 대조
merged = sql_result.merge(pd_result, on='region', suffixes=('_sql', '_pd'))
merged['diff'] = merged['total_sql'] - merged['total_pd']
print(merged[['region', 'total_sql', 'total_pd', 'diff']])
