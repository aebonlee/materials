# 1단계 — timeseries.py 끝에 이어 붙입니다
ts = m.set_index('order_date').sort_index()
print('인덱스 타입:', ts.index.dtype)
print('기간:', ts.index.min().date(), '~', ts.index.max().date())
print(ts.head(2))
