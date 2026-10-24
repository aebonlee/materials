# 내 컴퓨터에 mysql 클라이언트가 있다면
mysql -h 127.0.0.1 -P 3306 -uroot -pdataeng123 shop -e "SELECT VERSION();"

# 없어도 됩니다 — 다른 컨테이너를 클라이언트로 써서 확인할 수 있습니다
# (--add-host 줄은 리눅스·WSL2 도커 엔진에서 필요하고, Docker Desktop 에서는 있어도 결과가 같습니다)
docker run --rm --add-host=host.docker.internal:host-gateway mysql:9.7 \
  mysql -h host.docker.internal -P 3306 -uroot -pdataeng123 shop \
  -e "SELECT VERSION();"
