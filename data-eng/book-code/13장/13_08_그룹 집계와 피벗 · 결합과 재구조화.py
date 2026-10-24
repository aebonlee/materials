# 2단계(비교) — analyze.py 끝에 이어 붙입니다
# 리스트로 넘기면 열 이름이 두 겹이 됩니다
multi = df.groupby('category').agg({'amount': ['sum', 'mean']})
print(multi.columns.tolist())      # [('amount','sum'), ('amount','mean')]
print(multi.head(2))
