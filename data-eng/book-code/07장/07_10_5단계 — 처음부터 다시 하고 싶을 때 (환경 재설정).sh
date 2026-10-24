# 컨테이너 지우기
docker rm -f de-mysql

# 볼륨 지우기 — 이 장에서 넣은 데이터와 비밀번호가 함께 지워집니다(되돌릴 수 없음)
docker volume rm de-mysql-data

# 확인 — 아무 줄도 안 나오면 끝
docker ps -a --filter name=de-mysql
docker volume ls --filter name=de-mysql
