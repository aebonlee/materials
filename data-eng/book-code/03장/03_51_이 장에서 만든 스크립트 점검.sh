cd ~/data-eng/week1
ls *.sh

# 하나씩 돌려 종료 코드까지 확인
for s in greet.sh check_file.sh count_errors.sh scan_logs.sh; do
  echo "--- $s ---"
  case "$s" in
    greet.sh)        ./$s 홍길동 ;;
    check_file.sh)   ./$s access.log ;;
    count_errors.sh) ./$s access.log ;;
    scan_logs.sh)    ./$s ;;
  esac
  echo "종료 코드: $?"
done
