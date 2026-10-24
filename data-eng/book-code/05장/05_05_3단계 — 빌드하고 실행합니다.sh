# 이미지 빌드 (태그: data-app:0.1)
docker build -t data-app:0.1 .

# 만들어진 이미지 확인
docker images data-app

# 실행 (--rm: 종료 시 컨테이너 자동 삭제)
docker run --rm data-app:0.1
