# 이름만 다른 카탈로그 — uri·warehouse는 iceberg.properties와 같습니다
cat > catalog/iceberg2.properties <<'EOF'
connector.name=iceberg
iceberg.catalog.type=rest
iceberg.rest-catalog.uri=http://rest:8181
iceberg.rest-catalog.warehouse=s3://warehouse/
fs.s3.enabled=true
s3.endpoint=http://minio:9000
s3.region=us-east-1
s3.path-style-access=true
s3.aws-access-key=minioadmin
s3.aws-secret-key=minioadmin
EOF

docker compose restart trino
until docker compose exec trino trino --execute "SELECT 1" > /dev/null 2>&1; do sleep 2; done; echo "Trino 준비 완료"
