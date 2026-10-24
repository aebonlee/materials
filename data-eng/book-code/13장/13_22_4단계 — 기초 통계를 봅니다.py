# 4단계 — timeseries.py 끝에 이어 붙입니다
print(m[['price', 'quantity', 'amount']].describe().round(0))

# 분위수로 분포 보기
print('\n주문 금액 분위수')
print(m['amount'].quantile([0.25, 0.5, 0.75, 0.9, 0.99]).round(0))

# 지역별 평균과 편차
print('\n지역별')
print(m.groupby('region')['amount'].agg(['mean', 'std', 'count']).round(0))
