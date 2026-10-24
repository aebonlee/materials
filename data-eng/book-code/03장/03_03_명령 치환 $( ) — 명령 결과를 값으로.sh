# 괄호 안 명령을 실행한 결과가 그 자리에 들어옵니다
today=$(date +%Y%m%d)
echo "오늘은 $today"

# 파일 줄 수를 변수에 담기
lines=$(wc -l < access.log)
echo "줄 수: $lines"

# 백틱 `명령`도 같은 뜻이지만 옛 문법입니다. $( )를 쓰세요 — 중첩이 됩니다.
