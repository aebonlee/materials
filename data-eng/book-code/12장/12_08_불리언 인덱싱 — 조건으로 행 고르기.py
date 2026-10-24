# 예시 — 「데이터 불러오기와 저장」 절 3단계에서 df를 만든 뒤 돌려 봅니다
# 조건식 자체는 True/False의 Series를 만듭니다
mask = df['price'] > 100000
print(mask.head())        # 0 True, 1 True, ... (앞 5행은 모두 10만 원 초과)

# 그 목록을 대괄호에 넣으면 True 인 행만 남습니다
print(df[mask].shape)

# 조건을 여러 개 잇기 — 각 조건을 괄호로 감싸고 & | 로 잇습니다
df[(df['price'] > 100000) & (df['quantity'] >= 3)]
