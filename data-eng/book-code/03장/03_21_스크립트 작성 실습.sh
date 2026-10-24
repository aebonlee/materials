# 3단계처럼 먼저 bash로 들어갑니다 — macOS 기본 zsh는 ① 결과가 다릅니다(2가 나옵니다)
bash

# ① cat | while로 쓰면 센 값이 사라집니다
printf "a\nb\n" > two.txt
n=0; while read -r l; do n=$((n+1)); done < two.txt
echo "$n"
#   2
n=0; cat two.txt | while read -r l; do n=$((n+1)); done
echo "$n"
#   0              ← 딴 방에서 세고 나왔다

# ② ERROR*는 글롭 — 정규식의 .*가 아닙니다
line="ERROR abc"; case "$line" in ERROR*)  echo "걸림";; *) echo "안 걸림";; esac
#   걸림
line="XERRORX";   case "$line" in ERROR*)  echo "걸림";; *) echo "안 걸림";; esac
#   안 걸림        ← 앞이 다르면 안 걸린다
line="ERROR";     case "$line" in ERROR.*) echo "걸림";; *) echo "안 걸림";; esac
#   안 걸림        ← 정규식이었다면 걸렸을 것

# ③ -r이 없으면 역슬래시가 먹힙니다
printf '%s\n' 'C:\temp\x' > bs.txt
read l < bs.txt;    printf '%s\n' "$l"
#   C:tempx
read -r l < bs.txt; printf '%s\n' "$l"
#   C:\temp\x

exit              # 원래 셸로 돌아옵니다
