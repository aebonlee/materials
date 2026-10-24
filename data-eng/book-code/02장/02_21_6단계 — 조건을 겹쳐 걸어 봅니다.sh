# 또는(OR) — ERROR 이거나 WARN. -E는 | 를 "또는"으로 읽게 합니다
grep -E 'ERROR|WARN' access.log

# 그리고(AND) — grep에 AND 옵션은 없습니다. 파이프로 이어서 거릅니다
grep INFO access.log | grep kim

# 앞뒤 맥락 — 걸린 줄의 앞 1줄(-B)과 뒤 1줄(-A)까지 함께
grep -B 1 -A 1 WARN access.log
