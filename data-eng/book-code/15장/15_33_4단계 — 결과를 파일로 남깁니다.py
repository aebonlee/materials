# 4단계 — roundtrip.py 끝에 이어 붙입니다
import os

# Pandas로 저장
users.to_parquet('user_segments.parquet', index=False)

# DuckDB로 저장 (DataFrame을 그대로 COPY)
duckdb.sql("COPY (SELECT * FROM seg) TO 'segment_summary.parquet' (FORMAT parquet)")

for f in ['user_segments.parquet', 'segment_summary.parquet']:
    print(f, f'{os.path.getsize(f)/1024:.1f} KB')
