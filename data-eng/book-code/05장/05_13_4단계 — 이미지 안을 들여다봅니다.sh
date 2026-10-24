# 층별로 어떤 명령이 얼마의 크기를 만들었는지
docker history data-app:0.3

# fat 버전과 비교
docker history data-app:fat | head -n 8

# 이미지 안에 내 파일이 잘 들어갔는지 직접 확인
docker run --rm data-app:0.3 ls -la /app
