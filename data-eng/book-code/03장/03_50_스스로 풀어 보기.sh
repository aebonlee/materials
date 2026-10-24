# backup.sh의 dest를 정하는 부분을 바꿉니다
base="backup_$(date +%Y%m%d)"
dest="$base"
n=2
while [ -e "$dest" ]; do
  dest="${base}_${n}"
  n=$((n + 1))
done

# 확인 — 세 번 돌리면 _2 · _3 · _4가 생깁니다(이미 있던 backup_날짜까지 네 개)
./backup.sh logs ; ./backup.sh logs ; ./backup.sh logs
ls -d backup_*
