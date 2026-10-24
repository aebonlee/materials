# 목록을 하나씩
for f in *.log; do
  echo "처리 중: $f"
done

# 숫자 범위
for i in 1 2 3; do
  echo "$i 번째"
done

# 파일을 한 줄씩 읽기 (실무에서 아주 자주 씁니다)
while read -r line; do
  echo "줄: $line"
done < access.log
