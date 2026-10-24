cat > .dockerignore << 'EOF'
# 빌드에 필요 없는 것들 — 전송에서 빠집니다
Dockerfile.bad
__pycache__/
*.pyc
.git/
*.log
EOF

# 다시 빌드하며 첫 줄의 transferring context 크기를 비교해 보세요
docker build -t data-app:0.3 .
