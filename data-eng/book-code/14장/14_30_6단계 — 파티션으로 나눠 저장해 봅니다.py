# 6단계 — speed.py 끝에 이어 붙입니다
duckdb.sql("""
    COPY (SELECT *, CAST(ts AS DATE) AS day FROM 'events.csv')
    TO 'events_parted'
    (FORMAT parquet, PARTITION_BY (event_type), COMPRESSION zstd, OVERWRITE_OR_IGNORE)
""")
print('파티션 저장 완료')
