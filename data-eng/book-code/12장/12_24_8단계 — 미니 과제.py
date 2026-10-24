# 8단계(미니 과제 정답 예시) — transform.py 끝에 이어 붙입니다
for cat in df['category'].unique():
    sub = df[df['category'] == cat]
    print(cat, round(sub['amount'].mean()))

print(df[df['quantity'] == 5][['order_id', 'amount']].head())
print(df.sort_values('amount', ascending=False).head(10)[['order_id', 'category', 'amount']])
