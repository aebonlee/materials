# > 는 덮어쓰기
grep ERROR access.log > errors.txt
wc -l < errors.txt

# >> 는 이어 붙이기
grep WARN access.log >> errors.txt
wc -l < errors.txt

# tee는 화면에도 보여 주면서 파일에도 남깁니다
cut -d ' ' -f 1 access.log | sort | uniq -c | sort -rn | tee level_count.txt
