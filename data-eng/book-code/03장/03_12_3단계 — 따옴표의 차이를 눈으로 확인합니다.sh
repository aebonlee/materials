# ① bash로 들어갑니다 (세 운영체제 모두 이 한 줄로 같아집니다)
bash

# ② 공백이 든 이름의 파일을 하나 만듭니다
cd ~/data-eng/week1
touch "my report.txt"
f="my report.txt"

# ③ 따옴표 없이 — 「my」 와 「report.txt」 두 개로 쪼개져 둘 다 실패합니다
ls $f
#   ls: cannot access 'my': No such file or directory
#   ls: cannot access 'report.txt': No such file or directory
#   (macOS는 「ls: my: No such file or directory」 꼴로 나옵니다)

# ④ 따옴표를 씌우면 통째로 하나입니다
ls "$f"
#   my report.txt

# ⑤ 정리하고 원래 셸로 돌아옵니다
rm "my report.txt"
exit
