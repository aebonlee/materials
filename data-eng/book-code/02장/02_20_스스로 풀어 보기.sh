grep 'user=' access.log | cut -d ' ' -f 3 | sort | uniq -c | sort -k1,1rn -k2,2

# 결과
#   2 user=kim
#   1 user=lee
#   1 user=park
