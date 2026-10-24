docker run -d --name web2 -p 8080:80 nginx:1.27

# 컨테이너 내부 셸 접속 (-it: 대화형 터미널)
docker exec -it web2 bash
