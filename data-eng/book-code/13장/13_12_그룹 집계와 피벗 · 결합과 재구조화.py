# 5단계(validate) — analyze.py 끝에 이어 붙입니다
# validate를 주면 여기서 멈춥니다
try:
    df.merge(bad, on='customer_id', how='left', validate='many_to_one')
except Exception as e:
    print('예상대로 차단:', type(e).__name__)
    print(e)
