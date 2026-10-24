shellcheck scan_logs.sh
echo $?            # 0 — 아무것도 안 나오면 통과입니다

# 지금까지 만든 것을 한꺼번에
shellcheck *.sh
echo $?            # 지적할 것이 있으면 1
