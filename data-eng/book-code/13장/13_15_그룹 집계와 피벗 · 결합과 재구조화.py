# 6단계(다른 관점) — analyze.py 끝에 이어 붙입니다
# 건수로 채운 교차표 · 평균으로 채운 교차표
print(m.pivot_table(index='region', columns='category',
                    values='order_id', aggfunc='count', fill_value=0))
print(m.pivot_table(index='region', columns='category',
                    values='amount', aggfunc='mean', fill_value=0).round(0))
