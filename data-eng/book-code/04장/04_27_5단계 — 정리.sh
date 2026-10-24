# 실습용 컨테이너 정리
docker stop pg_novol && docker rm pg_novol

# pg는 정지만 해 둡니다 (Compose 실습 전에 5432 포트가 비어 있는지 확인한 뒤 정리합니다)
docker stop pg

docker ps -a
docker volume ls
