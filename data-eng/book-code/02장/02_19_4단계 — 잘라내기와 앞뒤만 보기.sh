# 앞 3줄 / 뒤 2줄
head -n 3 access.log
tail -n 2 access.log

# 공백으로 잘라 두 번째 칸만 (-d 구분자, -f 몇 번째)
cut -d ' ' -f 2 access.log

# 로그 레벨(첫 칸)만 뽑아 집계
cut -d ' ' -f 1 access.log | sort | uniq -c | sort -rn
