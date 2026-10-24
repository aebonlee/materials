# 5단계 — analyze.py 끝에 이어 붙입니다
# 고객 마스터에 중복 행을 심습니다 (실무에서 흔한 사고)
bad = pd.concat([customers, customers.head(5)], ignore_index=True)
print('customers 원본:', len(customers), '/ 중복 심은 것:', len(bad))

# validate 없이 — 조용히 불어납니다
m_bad = df.merge(bad, on='customer_id', how='left')
print('결합 후 행 수:', len(m_bad), '(원본', len(df), ')')
print('매출 합계 원본:', int(df['amount'].sum()))
print('매출 합계 결합후:', int(m_bad['amount'].sum()), '← 부풀려졌습니다')
