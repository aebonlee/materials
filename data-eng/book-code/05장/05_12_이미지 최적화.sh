cat > Dockerfile.multi << 'EOF'
FROM python:3.12 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/deps -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /deps /deps
ENV PYTHONPATH=/deps
COPY . .
CMD ["python", "app.py"]
EOF

docker build -t data-app:multi -f Dockerfile.multi .
docker run --rm data-app:multi
docker images data-app
