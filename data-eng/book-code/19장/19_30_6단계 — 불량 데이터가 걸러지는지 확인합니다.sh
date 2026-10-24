cat > data/orders_bad.csv <<'EOF'
order_id,customer,amount,order_date,channel
6,bad1,-5000,2026-08-03,web
,bad2,10000,2026-08-03,web
7,ok,18000,2026-08-03,app
EOF

docker compose exec mc mc cp /data/orders_bad.csv local/raw/orders/orders_bad.csv
