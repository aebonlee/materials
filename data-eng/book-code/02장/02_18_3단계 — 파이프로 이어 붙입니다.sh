# 같은 줄끼리 묶어 개수를 세고, 많은 순으로 정렬
#   sort  : 같은 줄을 이웃하게 모읍니다 (uniq는 이웃한 것만 묶습니다)
#   uniq -c : 묶으면서 개수를 앞에 붙입니다
#   sort -rn : 숫자(n) 기준 내림차순(r)
sort access.log | uniq -c | sort -rn

# 한 단계씩 끊어 보면 무슨 일이 일어나는지 보입니다
sort access.log
sort access.log | uniq -c
