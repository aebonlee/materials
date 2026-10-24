# 백그라운드(-d)로 실행, 내 8080 포트를 컨테이너 80에 연결
docker run -d --name web -p 8080:80 nginx:1.27

# 실행 중인 컨테이너 확인
docker ps

# 접속 확인 (브라우저에서 http://localhost:8080도 열어 보기)
curl http://localhost:8080

# 로그 확인
docker logs web

# 정지 → 정지된 것까지 보기 → 삭제
docker stop web
docker ps
docker ps -a
docker rm web
docker ps -a
