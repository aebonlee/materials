# count_errors.sh의 마지막에 추가
if [ "$errors" -ge 1 ]; then
  exit 2
fi
exit 0

# 확인
./count_errors.sh access.log ; echo $?     # 2
grep -v ERROR access.log > clean.log
./count_errors.sh clean.log ; echo $?       # 0
