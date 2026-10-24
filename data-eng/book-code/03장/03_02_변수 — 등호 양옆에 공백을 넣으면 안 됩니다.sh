# 올바른 선언 (공백 없음)
name="데이터"
count=5

# 틀린 선언 — command not found가 납니다
# name = "데이터"

# 사용할 때는 앞에 $
echo "$name 엔지니어링"
echo "총 ${count}개"     # 중괄호는 변수명의 경계를 분명히 할 때
