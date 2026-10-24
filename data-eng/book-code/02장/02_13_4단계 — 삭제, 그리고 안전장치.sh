cd ~/data-eng/week1

# 연습용 파일·폴더 만들기
touch trash1.txt trash2.txt
mkdir -p trashdir
ls

# 하나씩 확인하며 삭제 (-i: 물어봅니다. y를 입력)
rm -i trash1.txt

# 그냥 삭제
rm trash2.txt

# 폴더는 -r(재귀)이 필요합니다
rm -r trashdir
ls
