# 깨지는 것을 먼저 눈으로 봅니다
./daily_report.sh ; echo $?        # 2
cat report_*.txt                   # 머리글 + 두 줄, 세 줄만 있습니다

# daily_report.sh에서 그 줄만 고칩니다
#   전:  ./count_errors.sh "$log" >> "$out"
#   후: 2(ERROR 있음)만 허용, 그 밖의 실패는 그대로 멈춤
./count_errors.sh "$log" >> "$out" || [ $? -eq 2 ]

# 확인 — 정상 로그는 0, 없는 파일은 count_errors.sh의 1에서 바로 멈춥니다
./daily_report.sh ; echo $?               # 0
./daily_report.sh no-such.log ; echo $?   # 1
