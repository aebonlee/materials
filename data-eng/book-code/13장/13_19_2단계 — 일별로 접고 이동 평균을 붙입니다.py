# 2단계 — timeseries.py 끝에 이어 붙입니다
daily = ts['amount'].resample('D').sum()
weekly_trend = daily.rolling(7).mean()

print('일별 매출 (마지막 3일)')
print(daily.tail(3))
print('7일 이동 평균 (마지막 3일)')
print(weekly_trend.round(0).tail(3))

print('daily 행 수:', len(daily))
print('rolling 행 수:', len(weekly_trend), '← 같습니다')
