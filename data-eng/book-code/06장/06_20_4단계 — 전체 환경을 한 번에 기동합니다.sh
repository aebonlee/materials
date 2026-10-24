# docker run으로 띄웠던 pg 컨테이너가 5432를 쓰고 있으면 먼저 정지
docker stop pg 2>/dev/null

# 빌드 + 기동을 한 번에
docker compose up -d --build

# 서비스 상태 확인
docker compose ps -a

# app 서비스 출력 확인
docker compose logs app
