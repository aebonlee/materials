# 3단계 — transform.py 끝에 이어 붙입니다
# 어떤 값들이 들어 있나
print(df['category'].unique())
print(df['category'].nunique(), '가지')

# 각각 몇 건인가 — 오염이 눈에 보입니다
print(df['category'].value_counts())
