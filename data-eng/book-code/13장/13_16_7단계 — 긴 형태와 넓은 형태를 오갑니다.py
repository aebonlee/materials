# 7단계 — analyze.py 끝에 이어 붙입니다
# 넓은 형태(교차표) → 긴 형태
long = pv.reset_index().melt(id_vars='region',
                             var_name='category', value_name='amount')
print(long.head())
print('행 수:', len(long), '(지역 4 × 카테고리 4)')

# 긴 형태 → 다시 넓게
wide = long.pivot(index='region', columns='category', values='amount')
print('원래대로 돌아왔는가:', wide.equals(pv))
