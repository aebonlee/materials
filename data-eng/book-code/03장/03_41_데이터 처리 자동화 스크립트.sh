# 준비 — 있는 파일 하나, 없는 이름 하나
touch 있는파일.txt

# ① 그냥 실행 — 둘 다 화면에 나옵니다
ls 있는파일.txt 없는파일.txt
#   ls: cannot access '없는파일.txt': No such file or directory   ← 2번(오류)
#   있는파일.txt                                   ← 1번(정상)

# ② > /dev/null — 정상만 버립니다. 오류는 그대로 보입니다
ls 있는파일.txt 없는파일.txt > /dev/null
#   ls: cannot access '없는파일.txt': No such file or directory
#   (macOS는 「ls: 없는파일.txt: No such file or directory」)

# ③ 2> /dev/null — 오류만 버립니다. 정상은 그대로 보입니다
ls 있는파일.txt 없는파일.txt 2> /dev/null
#   있는파일.txt

# ④ > /dev/null 2>&1 — 둘 다 버립니다. 아무것도 안 나옵니다
ls 있는파일.txt 없는파일.txt > /dev/null 2>&1
