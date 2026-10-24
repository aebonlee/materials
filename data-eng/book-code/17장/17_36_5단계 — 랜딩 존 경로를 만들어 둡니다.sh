cat > data/orders_2026-08-01.csv << 'EOF'
order_id,customer,amount,order_date,channel
1,kim,15000,2026-08-01,web
2,lee,32000,2026-08-01,app
EOF

docker compose exec mc mc cp /data/orders_2026-08-01.csv local/raw/orders/orders_2026-08-01.csv
