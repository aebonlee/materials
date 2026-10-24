# 5단계(습관) — analyze.py 끝에 이어 붙입니다
# 결합 전에 키 중복을 미리 확인하는 습관
print('오른쪽 키 중복 건수:', bad['customer_id'].duplicated().sum())
print('정상 마스터 중복 건수:', customers['customer_id'].duplicated().sum())
