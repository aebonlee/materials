# 3단계 — timeseries.py 끝에 이어 붙입니다
weekly = ts['amount'].resample('W').sum()
monthly = ts['amount'].resample('ME').agg(['sum', 'mean', 'count'])

print('주별 매출')
print(weekly)
print('\n월별 요약')
print(monthly.round(0))
