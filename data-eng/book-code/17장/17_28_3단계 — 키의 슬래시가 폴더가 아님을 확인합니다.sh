echo "2026-08-01 data" > data/d1.csv
echo "2026-08-02 data" > data/d2.csv

docker compose exec mc mc cp /data/d1.csv local/raw/demo/dt=2026-08-01/part-0.csv
