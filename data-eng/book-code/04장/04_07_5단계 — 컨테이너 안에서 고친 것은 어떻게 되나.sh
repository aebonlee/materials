# 컨테이너 안의 웹 페이지를 바꿔 봅니다
docker exec web2 bash -c 'echo "<meta charset=utf-8><h1>내가 고친 페이지</h1>" > /usr/share/nginx/html/index.html'
curl http://localhost:8080

# 컨테이너를 지우고 같은 이미지로 다시 만듭니다
docker stop web2 && docker rm web2
docker run -d --name web2 -p 8080:80 nginx:1.27
curl http://localhost:8080
