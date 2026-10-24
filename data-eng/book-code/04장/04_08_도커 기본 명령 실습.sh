# ① 둘 다 강제로 치웁니다 (없으면 오류가 나지만 무시해도 됩니다)
docker rm -f web web2

# ② 새로 띄우고 고칩니다
docker run -d --name web2 -p 8080:80 nginx:1.27
docker exec web2 bash -c 'echo "<meta charset=utf-8><h1>내가 고친 페이지</h1>" > /usr/share/nginx/html/index.html'

# ③ 컨테이너 안 파일부터 확인합니다 — 여기서 바뀌어 있어야 합니다
docker exec web2 cat /usr/share/nginx/html/index.html
#   <meta charset=utf-8><h1>내가 고친 페이지</h1>

# ④ 그다음 밖에서
curl http://localhost:8080
