mkdir -p ~/data-eng/week1/app
cd ~/data-eng/week1/app

cat > app.py << 'EOF'
import platform

print("데이터 파이프라인 앱이 실행되었습니다.")
print("파이썬 버전:", platform.python_version())
EOF

cat > requirements.txt << 'EOF'
requests
EOF

cat > Dockerfile << 'EOF'
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
EOF

ls
