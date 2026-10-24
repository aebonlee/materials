# 실습 파일 만들기
printf 'kim\nlee\nkim\npark\nkim\nlee\n' > access.log

# 사용자별 횟수, 많은 순
sort access.log | uniq -c | sort -rn
