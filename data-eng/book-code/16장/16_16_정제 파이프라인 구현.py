# 5단계(검사기 깨뜨리기) — validate_test.py 끝에 이어 붙입니다
# 일부러 나쁜 값을 넣어 검사기가 실제로 잡는지 확인합니다
bad = cleaned.copy()
bad.loc[0, 'price'] = -1000
bad.loc[1, 'category'] = '알수없음'
print(validate(bad))
