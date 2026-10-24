cd ~/data-eng/week3
ls -lh orders_clean.parquet quality_report.csv quality_report.md clean_orders.py

# 결과물을 완성하기 전 마지막으로 처음부터 재현되는지
rm -f orders_clean.parquet
python3 clean_orders.py
python3 quality_report.py
ls -lh orders_clean.parquet quality_report.csv
