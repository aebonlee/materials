cd ~/data-eng

# 이름으로 찾기
#   "*.sh"의 *는 「아무 글자나 몇 개든」이라는 뜻입니다
#   그래서 .sh로 끝나는 이름 전부가 걸립니다
find . -name "*.sh"

# 디렉터리만 / 파일만
find . -type d
find . -type f

# 파일 개수 세기 (find 결과를 wc로 넘깁니다 — 바로 뒤 「텍스트 처리와 파이프라인」의 예고편입니다)
find . -type f | wc -l

# 용량 확인
du -sh ~/data-eng
