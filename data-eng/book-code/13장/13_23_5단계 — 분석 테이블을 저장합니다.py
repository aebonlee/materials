# 5단계 — timeseries.py 끝에 이어 붙입니다
m.to_parquet('orders_enriched.parquet', index=False)
print('저장 완료:', len(m), '행,', len(m.columns), '열')
print('열 목록:', m.columns.tolist())
