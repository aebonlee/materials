# 5단계 — speed.py 끝에 이어 붙입니다
for comp in ['zstd', 'snappy', 'gzip']:
    out = f'events_{comp}.parquet'
    duckdb.sql(f"COPY (SELECT * FROM 'events.csv') TO '{out}' (FORMAT parquet, COMPRESSION {comp})")
    size = os.path.getsize(out) / 1024 / 1024
    t = bench(f"SELECT event_type, sum(value) FROM '{out}' GROUP BY event_type")
    print(f'{comp:8s}  {size:6.1f} MB   {t:.3f} 초')
