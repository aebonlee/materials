cd ~/data-eng/week1

# 빈 파일 생성
touch notes.txt

# 복사 (원본은 그대로 남습니다)
cp notes.txt notes_backup.txt
ls

# logs/ 로 이동 (원본이 사라집니다)
mv notes_backup.txt logs/
ls
ls logs

# 이름 변경도 mv로 합니다 (같은 자리에서 옮기는 셈)
mv notes.txt memo.txt
ls
