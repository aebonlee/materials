# ERROR가 들어간 줄만
grep ERROR access.log

# 개수만 (-c)
grep -c ERROR access.log

# 대소문자 무시 (-i)
grep -i error access.log

# ERROR가 아닌 줄만 (-v: 반대로)
grep -v ERROR access.log

# 줄 번호까지 (-n)
grep -n ERROR access.log
