# app.py에 한 줄 추가
echo 'print("이 줄은 재빌드 실험용입니다.")' >> app.py

# 재빌드 — 빌드 로그에서 CACHED 표시를 찾아보세요
docker build -t data-app:0.2 .
docker run --rm data-app:0.2
