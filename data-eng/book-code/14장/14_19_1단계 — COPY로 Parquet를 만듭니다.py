# speed.py — 1~6단계를 이 파일에 이어 붙입니다
import os
import time
import duckdb

duckdb.sql("""
    COPY (SELECT * FROM 'events.csv')
    TO 'events.parquet' (FORMAT parquet, COMPRESSION zstd)
""")
print('변환 완료')
