# 3단계 — speed.py 끝에 이어 붙입니다
def bench(sql, rounds=3):
    times = []
    for _ in range(rounds):
        t0 = time.perf_counter()
        duckdb.sql(sql).fetchall()
        times.append(time.perf_counter() - t0)
    return sum(times) / len(times)

csv_t = bench("SELECT event_type, sum(value) FROM 'events.csv' GROUP BY event_type")
pq_t  = bench("SELECT event_type, sum(value) FROM 'events.parquet' GROUP BY event_type")

print(f'CSV     질의: {csv_t:.3f} 초')
print(f'Parquet 질의: {pq_t:.3f} 초')
print(f'차이        : {csv_t/pq_t:.1f}배')
