# 6단계 — analyze.py 끝에 이어 붙입니다
pv = m.pivot_table(index='region', columns='category',
                   values='amount', aggfunc='sum', fill_value=0)
print(pv)
print('교차표 총합 == 전체 매출:', pv.to_numpy().sum() == m['amount'].sum())
