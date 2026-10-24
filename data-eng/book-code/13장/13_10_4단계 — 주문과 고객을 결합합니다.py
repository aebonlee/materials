# 4단계 — analyze.py 끝에 이어 붙입니다 (customers는 파일 머리에서 이미 읽었습니다)
m = df.merge(customers, on='customer_id', how='left',
             validate='many_to_one')
print('결합 전:', len(df), '행 / 결합 후:', len(m), '행')
print('region 결측:', m['region'].isna().sum(), '건')
