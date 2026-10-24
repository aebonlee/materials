# 컨테이너 지우기
docker rm -f de-mongo

# 볼륨 지우기 — logdb의 모든 문서가 함께 지워집니다(되돌릴 수 없음)
docker volume rm de-mongo-data

# 확인 — 제목 줄만 나오면 끝
docker ps -a --filter name=de-mongo
docker volume ls --filter name=de-mongo
