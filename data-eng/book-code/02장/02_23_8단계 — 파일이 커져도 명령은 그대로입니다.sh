# 같은 로그를 100번 이어 붙여 800줄짜리를 만듭니다
#   $( )는 괄호 안 명령을 먼저 실행해 그 결과를 그 자리에 끼워 넣습니다
#   seq 1 100은 1부터 100까지 숫자를 냅니다 — 반복문은 3장에서 제대로 다룹니다
for i in $(seq 1 100); do cat access.log; done > big.log
wc -l < big.log

# 4단계에서 쓴 명령을 파일 이름만 바꿔 그대로 돌려 봅니다
cut -d ' ' -f 1 big.log | sort | uniq -c | sort -rn
