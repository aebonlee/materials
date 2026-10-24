# COPY . . 를 먼저 쓰는 나쁜 순서
cat > Dockerfile.bad << 'EOF'
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
EOF

# 처음 빌드 (pip install이 실제로 돌아 오래 걸리는 것이 정상입니다)
docker build -t data-app:bad -f Dockerfile.bad .

# 코드 한 줄 고치고 각각 재빌드해 시간 비교
echo 'print("두 번째 실험")' >> app.py

time docker build -t data-app:good2 -f Dockerfile .
time docker build -t data-app:bad2  -f Dockerfile.bad .
