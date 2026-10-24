cd ~/data-eng/week1

# week1 환경 내리기 (볼륨은 남겨 둡니다)
docker compose down

# docker run으로 띄웠던 pg 컨테이너가 남아 있으면 정리
docker rm pg 2>/dev/null

# 남은 것 확인
docker ps -a
docker images

# 제2부 폴더 미리 만들어 두기
mkdir -p ~/data-eng/week2
