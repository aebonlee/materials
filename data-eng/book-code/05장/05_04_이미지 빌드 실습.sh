cd ~/data-eng/week1/app

# 위 내용을 파일로 저장 (편집기를 써도 됩니다)
cat > Dockerfile << 'EOF'
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
EOF

cat Dockerfile
