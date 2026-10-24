# ① fi를 빠뜨리면
bash -c 'if [ -f access.log ]; then echo "있음"'
#   bash: -c: line 2: syntax error: unexpected end of file   (bash 판에 따라 앞부분이 조금 다릅니다)
#   → "파일이 끝났는데 닫는 말이 안 나왔다"는 뜻입니다

# ② then 앞의 세미콜론을 빠뜨리면
bash -c 'if [ -f access.log ] then echo "있음"; fi'
#   bash: -c: line 1: syntax error near unexpected token `fi'

# ③ 줄을 바꿔 쓰면 세미콜론이 필요 없습니다
if [ -f access.log ]
then
  echo "있음"
fi
