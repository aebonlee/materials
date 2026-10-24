# 이번 실습 컨테이너 정리
docker stop web2
docker rm web2

# 정지된 컨테이너 한꺼번에 정리
docker container prune

# 지금 상태 확인 — 아무것도 안 남아야 합니다
docker ps -a
