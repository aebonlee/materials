# 컨테이너 정지 (데이터는 볼륨에 남습니다)
docker stop de-mongo
# de-mysql은 제3부에는 쓰지 않습니다 — docker stop de-mysql로 꺼 두어도 데이터는 볼륨에 남고, 필요할 때 docker start de-mysql

docker ps -a | grep de-
mkdir -p ~/data-eng/week3
