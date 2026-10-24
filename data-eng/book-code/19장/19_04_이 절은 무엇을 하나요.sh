# 순서만 미리 봅니다 — 줄 앞의 # 때문에 붙여 넣어도 실행되지 않습니다
# 1) 원천 데이터 적재 2단계 — cat > data/orders_2026-08-02.csv … → mc cp로 raw/orders/ 에
# 2) ETL 1·2단계 — cat > scripts/etl_bad.py << 'EOF' … EOF, cat > scripts/etl_orders.py << 'EOF' … EOF
# 3) 그 뒤부터 spark-submit --packages … /home/iceberg/scripts/etl_orders.py가 됩니다
