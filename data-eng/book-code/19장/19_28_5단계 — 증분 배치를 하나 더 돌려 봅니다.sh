cat > data/orders_2026-08-03.csv <<'EOF'
order_id,customer,amount,order_date,channel
4,choi,61000,2026-08-03,app
5,jung,24000,2026-08-03,web
EOF

docker compose exec mc mc cp /data/orders_2026-08-03.csv local/raw/orders/orders_2026-08-03.csv
