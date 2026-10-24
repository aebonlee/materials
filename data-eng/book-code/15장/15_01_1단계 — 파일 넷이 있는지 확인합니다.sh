cd ~/data-eng/week3
source .venv/bin/activate        # Windows(WSL2)·macOS·리눅스 같습니다
ls -lh events.parquet orders_step1.parquet customers.csv orders_enriched.parquet
python3 -c "import duckdb; print(duckdb.sql(\"SELECT count(*) FROM 'events.parquet'\").fetchone()[0])"
