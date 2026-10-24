# 5단계 — transform.py 끝에 이어 붙입니다
# datetime이 되고 나면 .dt로 부품을 꺼낼 수 있습니다
df['year'] = df['order_date'].dt.year
df['month'] = df['order_date'].dt.month
df['weekday'] = df['order_date'].dt.day_name()

print(df[['order_date', 'year', 'month', 'weekday']].head(3))
print(df['weekday'].value_counts())
