# 지금까지 쓴 두 컨테이너 상태
docker ps -a | grep -E "de-mysql|de-mongo"

# 10장은 MySQL만 씁니다. Mongo는 정지해 메모리를 아껴도 됩니다.
# docker stop de-mongo

# 데이터는 볼륨에 남습니다
docker volume ls | grep de-
